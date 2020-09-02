import os
import time
from urllib import request
import json
from datetime import datetime, date
import cv2
from json import dumps
from subprocess import check_output
from telebot_send import send_msg

class FileManager(Exception):
    pass


parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Get the url
with open(os.path.join(parent_folder, "etc", "weighing_url.txt"), "r") as f:
    url = f.readline().replace("\n", "")


def get_saved_info():
    """
    Asks to the system for the number of saved images, their labels, and the current available space in the disk
    :return: string with the info.
    """

    def get_items_in_dir(dirname):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(dirname):
            files += [os.path.join(dirpath, file) for file in filenames]
        return files

    def get_size(files):
        return str(round(sum([os.path.getsize(x) for x in files]) / (1024 * 1024), 2)) + " MB"

    def make_info(path):
        items = get_items_in_dir(path)
        info = {"n_color": len(items), "size_color": get_size(items), "n_depth": None, "size_depth": None}
        items = list(map(lambda x: x.replace("color", "depth"), items))
        info["n_depth"] = len(items)
        info["size_depth"] = get_size(items)
        return info

    # paths to check the space
    paths = (os.path.join(parent_folder, "savings", "color", "lamb"),
             os.path.join(parent_folder, "savings", "color", "empty"),
             os.path.join(parent_folder, "savings", "color", "wrong"))
    info_msg = {"lamb": make_info(paths[0]), "empty": make_info(paths[1]), "wrong": make_info(paths[2])}

    # Ask to the (Linux) system and process the output
    space_available = str(check_output(['df', '-H', '/dev/sda1']), encoding="latin1").replace("Tama\u00c3\u00b1o",
                                                                                              "Total_Size").split()
    space_available = dict(zip(space_available[0:6], space_available[7:]))
    # formatting the result to make it pretty
    result = dumps(info_msg, indent=4) + "\n" + dumps(space_available, indent=4)
    return result


def get_weight():
    """
    Gets the current weight from the weighting machine where the lambs are placed
    :return float weight: the weight of the lamb
        or None: in case there's too much difference of time from the image taken and the url time
    """
    ts = time.time()
    try:
        json_url = request.urlopen(url)
        # Get the weight json info
        webdata = json.loads(json_url.read())
        # valid_ts = int(webdata["valid_weight"]["time"])
        current_ts = int(webdata["current_weight"]["time"])
        # We do a comparison in order to get a coherent weight for this current time.
        if 0 <= abs(current_ts - ts) <= 4:
            weight = float(webdata["current_weight"]["value"])
        else:
            print("\nThe weights taken by the json are too far from the current time\n")
            # There's a problem: don't save...?
            return None
    except Exception as e:
        print("\nProblem getting the json from the given url")
        print(e, "\n")
        return None
    return weight


def mkdirs(current_path, paths):
    """
    Creates folders in order to save the image files, json files and other necessary stuff
    :param current_path: parent folder where the script starts to make directories
    :param paths: collections of folder's names to create them recursively
    :return: the resulting path after the creations
    """
    current_path = os.path.join(current_path, str(paths[0]))
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    return mkdirs(current_path, paths[1:]) if len(paths) > 1 else current_path


def save_json(w_id, filenames, lamb_label, weight):
    """
    It saves the json file with info of the images
    :param w_id: string identifier of the image
    :param filenames: dictionary with the paths of the images
    :param lamb_label: string with the label of the lamb image (lamb, empty or wrong)
    :param weight: float with the weight of the current lamb
    """
    # Load and update the json
    weight_path = os.path.join(parent_folder, "savings", str(str(date.today()) + "_.json"))
    if os.path.exists(weight_path):
        with open(weight_path, "r") as f:
            data_weight = json.load(f)
    else:
        data_weight = {}

    data_weight[w_id] = {**filenames, "label": lamb_label, "weight": weight}

    # Save the weight of the new lamb image
    with open(weight_path, "w") as f:
        f.write(json.dumps(data_weight, sort_keys=True, indent=4))


def save_frames(cameras, lamb_label=None):
    """
    It saves the current frame to a file for each type of frame (2: color and depth)
    it also creates the folders needed to the specified path of the files.
    :param cameras: collection of RSCameras with color and depth images
        color image: numpy array with (640x480x3) of shape, the color image.
        depth image: numpy array with (640x480x1) of shape, the depth image.
    :param lamb_label: string with info of the lamb which is in the image.
    :return tuple(id, filename): string with the id of the frames (for the json file) (tmstamp_id),
        and the depth full filename with its path
    """
    today = str(date.today())

    if lamb_label is None or lamb_label == "":
        path_color = mkdirs(parent_folder, ("savings", "color", today))
        mkdirs(parent_folder, ("savings", "depth", today))
    else:
        path_color = mkdirs(parent_folder, ("savings", "color", lamb_label, today))
        mkdirs(parent_folder, ("savings", "depth", lamb_label, today))
    ts = time.time()
    tmstamp_id = str(datetime.fromtimestamp(ts)).replace(":", "-")
    filenames = {}
    for cam in cameras:
        color_frame = cam.color_image
        depth_frame = cam.depth_image

        filename = os.path.join(path_color, "{}_{}_{}_cam.png".format(tmstamp_id, "color", cam.name))

        filenames["path_color_{}_image".format(cam.name)] = filename.replace(str(parent_folder), "")

        filename = filename.replace(" ", "__")

        # Save frames
        correct, filename = __is_new_file_correct__(filename)
        if correct:
            pass # NO GUARDAMOS LAS IMAGENES DE COLOR ###################################################
            #cv2.imwrite(filename=filename, img=color_frame)
        else:
            raise FileManager("filename incorrect!!")
        # They both have a similar path, so this is more efficient; otherwise we should use the path_depth
        filename = filename.replace("color", "depth")
        filenames["path_depth_{}_image".format(cam.name)] = filename.replace(str(parent_folder), "")
        correct, filename = __is_new_file_correct__(filename)
        if correct:
            cv2.imwrite(filename=filename, img=depth_frame)
        else:
            raise FileManager("filename incorrect!!")
        # w_id = str(os.path.basename(filename))[0:-15]
    return tmstamp_id, filenames, ts


def save_info(cameras, weight, lamb_label=None):
    """
    If the disk usage is under 90%, it saves the frame as image files (color and depth), creates the folders requested to the files,
    and updates a json file with info of the frames for each day.
    :param cameras: collection of RSCameras with color and depth images
        color image: numpy array with (640x480x3) of shape, the color image.
        depth image: numpy array with (640x480x1) of shape, the depth image.
    :param lamb_label: string with info of the lamb which is in the image.
    :param weight: string with the info of the camera where the frames have been taken.
    """

    #check disk usage
    disk_usage = int(str(check_output(['df', '--output=pcent', '/dev/sda1']), encoding='utf-8').split("\n")[1].replace(" ","").replace("%",""))

    if disk_usage < 90:
        print("Disk usage: " + str(disk_usage) + "%")
        #saving frames and json data
        w_id, filenames, ts = save_frames(cameras, lamb_label)
        save_json(w_id, filenames, lamb_label, weight)
    else:
        print("[!] Disk usage over 90%\nNO FRAMES SAVED.")
        #Telegram msg to warn about disk usage
        send_msg(":double_exclamation_mark: Disk usage over 90% (" + str(disk_usage) + "%)")


def __is_new_file_correct__(file):
    dircorrect, dirname = __is_dir_file_correct__(file)
    file = os.path.join(str(dirname), str(os.path.basename(file)))
    if dircorrect:
        if not os.path.exists(file):
            return True, file
        else:
            # TODO. Not necessary and not required yet.
            # changes filename to "file (1), (2) ..."
            # right now it just overrides the file
            return True, file
    else:
        print("IS_FILE_CORRECT: error checking the file, file path not right")
        return False, None


def __is_dir_file_correct__(file):
    dirname = os.path.dirname(file)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    if os.path.exists(dirname) and os.path.isdir(dirname):
        if os.path.exists(dirname):
            return True, dirname
        else:
            return True, os.getcwd()
    else:
        raise FileManager("IS_DIR_FILE_CORRECT: error checking the file, file path not right")
