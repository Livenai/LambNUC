import os
import time
from urllib import request
import json
from datetime import datetime, date
import cv2
import numpy as np

class FileManager(Exception):
    pass


def get_saved_info():
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

    paths = (os.path.join(os.path.expanduser("~"), "LambNN", "savings", "color", "lamb"),
             os.path.join(os.path.expanduser("~"), "LambNN", "savings", "color", "no_lamb"),
             os.path.join(os.path.expanduser("~"), "LambNN", "savings", "color", "error"))
    info_msg = {"lamb": make_info(paths[0]), "empty": make_info(paths[1]), "error": make_info(paths[2])}
    from json import dumps
    from subprocess import check_output
    space_available = str(check_output(['df', '-H', '/dev/sda2']), encoding="latin1").replace("Tama\u00c3\u00b1o",
                                                                                              "Total_Size").split()
    space_available = dict(zip(space_available[0:6], space_available[7:]))

    result = dumps(info_msg, indent=4) + "\n" + dumps(space_available, indent=4)
    return result


def get_weight(path, ts):
    # get the url
    with open(os.path.join(path, "etc", "weighing_url.txt"), "r") as f:
        url = f.readline().replace("\n", "")
    try:
        json_url = request.urlopen(url)
        webdata = json.loads(json_url.read())
        valid_ts = int(webdata["valid_weight"]["time"])
        current_ts = int(webdata["current_weight"]["time"])
        if 0 <= abs(valid_ts - ts) <= 1:
            weight = float(webdata["valid_weight"]["value"])
        elif 0 <= abs(valid_ts - ts) <= 2:
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


def save_frames(color_frame, depth_frame, id_crotal=None, cam="cam01"):
    """
    It saves the current frame to a file for each type of frame (2: color and depth)
    it also creates the folders needed to the specified path of the files.
    :param color_frame: numpy array with (640x480x3) of shape, the color image.
    :param depth_frame: numpy array with (640x480x1) of shape, the depth image.
    :param id_crotal: string with the info of the lamb which is in the image.
    :param cam: string with the info of the camera where the frames have been taken.
    """
    today = time.today()
    mypath = os.path.join(os.path.expanduser('~'), 'LambNN')

    def mkdirs(current_path, paths):
        path = current_path
        for folder in paths:
            path = os.path.join(path, str(folder))
            if not os.path.exists(path):
                os.mkdir(path)
        return path

    if id_crotal is None:
        path_color = mkdirs(mypath, ("savings", "color", today))
        mkdirs(mypath, ("savings", "depth", today))
    else:
        path_color = mkdirs(mypath, ("savings", "color", id_crotal, today))
        mkdirs(mypath, ("savings", "depth", id_crotal, today))
    ts = time.time()
    # Get the weight only if there's a lamb in the image
    weight = get_weight(mypath, ts) if id_crotal == "lamb" or not bool(np.random.randint(10)) else None

    filename = os.path.join(path_color, "{}_{}_{}.png".format(datetime.fromtimestamp(ts), cam, "color"))

    # Load and update the json weights
    if weight is not None:
        w_id = str(os.path.basename(filename))[0:-15]
        weight_path = os.path.join(mypath, "savings", today, ".json")
        # Get the dict of weights or make a new one
        if os.path.exists(weight_path):
            with open(weight_path, "r") as f:
                data_weight = json.load(f)
        else:
            data_weight = {}
        data_weight[w_id] = weight
        # Save the weight of the new lamb image
        with open(weight_path, "w") as f:
            f.write(json.dumps(data_weight, sort_keys=True, indent=4))

    correct, filename = __is_new_file_correct__(filename)
    if correct:
        cv2.imwrite(filename=filename, img=color_frame)
    else:
        raise FileManager("filename incorrect!!")
    # They both have a similar path, so this is more efficient; otherwise we should use the path_depth
    filename = filename.replace("color", "depth")
    correct, filename = __is_new_file_correct__(filename)
    if correct:
        cv2.imwrite(filename=filename, img=depth_frame)
    else:
        raise FileManager("filename incorrect!!")


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
# return False, None
