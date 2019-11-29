import numpy as np

MAX_WHITES_ALLOWED = 20000


def filter_flies(depth_image_cropped):
    """
    Filter the given cropped image if it has relevant information or it doesn't
    :param depth_image_cropped: numpy array
    :return: the image or None in case the image is not relevant
    """
    white_pixels = np.sum(depth_image_cropped == 0.0)
    if white_pixels > MAX_WHITES_ALLOWED:
        return None
    else:
        return depth_image_cropped


def crop_image(in_array, x, y, h, w):
    """
    Crop a given image and return it with shape (h * w).
    :param in_array: array with the image
    :param x: starting coordinate x of the point for the interested area
    :param y: starting coordinate y of the point for the interested area
    :param h: height of the area
    :param w: width of the area
    :return numpy array with the result image
    """
    in_array = np.array(in_array)
    return in_array[y:y + h, x:x + w]


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
    img = crop_image(depth_image, 38, 102, 230, 503)
    img = filter_flies(depth_image_cropped=img)

    if img is not None:

        # predict
        img = np.array([img.reshape(480, 640, 1)])
        res = model.predict(img, verbose=0, use_multiprocessing=True)

        result_index = np.argmax(np.array(res))

        # TODO: the new predict will return a different set; not a 4 lenght array (it will be a 3-lenght arr.)
        if result_index == 0:
            print("\t CNN msg: There's a lamb. \t label:lamb")
            return True, "lamb"
        elif result_index == 1:
            print("\t CNN msg: There's no lamb. \t label:empty")
            # return not bool(np.random.randint(120)), "empty"
            return not bool(np.random.randint(60)), "empty"
        elif result_index == 2:
            print("\t CNN msg: There's prob. a lamb in a wrong position: \t label:wrong")
            # return not bool(np.random.randint(20)), "wrong"
            return not bool(np.random.randint(10)), "wrong"
        elif result_index == 3:
            print("\t CNN msg: Something is covering the camera. \t label:fly")
            # return not bool(np.random.randint(5)), "fly"
            return False, "fly"
        else:
            print("[!] Impossible print. Something is wrong in isThereALamb()")

        return True, "to_check"
    else:
        print("\t Alghtm msg: Flies detected!! \t-->\t label:fly")
        return False, "fly"
