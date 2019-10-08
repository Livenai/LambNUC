import os
import time
from PySide2.QtCore import QTime
from datetime import datetime, date
import cv2


class FileManager(Exception):
    pass


def save_frames(color_frame, depth_frame, id_crotal=None, cam="cam01"):
    ts = time.time()
    if id_crotal is not None:
        mypath = os.path.dirname(os.getcwd())

        def mkdirs(current_path, paths):
            path = current_path
            for folder in paths:
                path = os.path.join(path, str(folder))
                if not os.path.exists(path):
                    os.mkdir(path)
            return path

        if id_crotal is None:
            path_color = mkdirs(mypath, ("savings", "color", date.today()))
            path_depth = mkdirs(mypath, ("savings", "depth", date.today()))
        else:
            path_color = mkdirs(mypath, ("savings", "color", id_crotal, date.today()))
            path_depth = mkdirs(mypath, ("savings", "depth", id_crotal, date.today()))

        filename = os.path.join(path_color, "{}_{}_{}.png".format(datetime.fromtimestamp(ts), cam, "color"))

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
    return


def __is_new_file_correct__(file):
    dircorrect, dirname = __is_dir_file_correct__(file)
    file = os.path.join(str(dirname), str(os.path.basename(file)))
    if dircorrect:
        if not os.path.exists(file):
            return True, file
        else:
            # TODO
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
