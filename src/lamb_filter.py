import numpy as np
import cv2
import os



def cropWithZeros(in_array, x, y, h, w):
    """
    Crop a given image and refill it with zeros to keep the same shape.
    :param in_array: array with the image
    :param x: starting coordinate x of the point for the interesed area
    :param y: starting coordinate y of the point for the interesed area
    :param h: height of the area
    :param w: weidth of the area
    :return numpy array with the result image
    """
    in_array = np.array(in_array)
    shape = in_array.shape
    crop = in_array[y:y + h, x:x + w]
    bx = shape[0] - x - h
    by = shape[1] - y - w
    padding = ((x, bx), (y, by))
    return np.pad(crop, padding)


def isThereALamb(color_image, depth_image, model):
    """
    Asks if the current image has a lamb in a right position
    :param color_image: numpy array (640, 480, 3) shape RGB image.
    :param depth_image: numpy array (640, 480, 1) shape Depth image.
    :return: tuple(bool, string) string with the predicted image's label;
        it might be there's a part of a lamb in the image (still False).
    """
    # We only use the depth_image right now.
    # crop
    img = cropWithZeros(depth_image, 38, 102, 230, 503)

    # predict
    img = np.array([img.reshape(480, 640, 1)])
    res = model.predict(img, verbose=0, use_multiprocessing=True)

    result_index = np.argmax(np.array(res))

    if result_index == 0:
        print("\tThere's a lamb")
        return True, "lamb"
    elif result_index == 1:
        print("\tThere's no lamb")
        return not bool(np.random.randint(120)), "empty"
    elif result_index == 2:
        print("\tThere's something (prob. a lamb in a wrong position)")
        return not bool(np.random.randint(20)), "wrong"
    elif result_index == 3:
        print("\tSomething is covering the camera")
        return not bool(np.random.randint(1000)), "fly"
    else:
        print("[!] Impossible print. Something is wrong in isThereALamb()")

    return True, "to_check"
