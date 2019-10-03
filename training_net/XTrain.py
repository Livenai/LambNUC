import os
import sys
import numpy as np
import cv2


# system navigation
def get_items_in_dir(my_path=""):
    my_path = os.getcwd() if my_path == "" or my_path is None else my_path
    files = []
    for roots, dirs, items in os.walk(my_path):
        [files.append(os.path.join(roots, item)) for item in items]
    return files


def get_XTrain(depth=True):
    xtrain = []
    ytrain = []
    XY_train = []

    # walk packages...

    if depth:
        for item in range(423):  # 423 for example
            # new_file = np.empty((h, w, 4), dtype=np.uint8)
            pass
    else:
        # new_file = color_image = cv2.imread(filename)...
        pass

    # Shuffle / unsort XY_train matrix
    # NO: much better, shuffle the file path to each element; then load the image and make the train matrix's
    # unpack XY_train
    return xtrain, ytrain
