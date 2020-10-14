import numpy as np
import img_diff

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


def is_there_a_lamb(cameras, model):
    """
    Asks if the current image has a lamb in a right position
    :param cameras: collection of RSCameras which already have color and depth images
        color image: numpy array (640, 480, 3) shape RGB image.
        depth image: numpy array (640, 480, 1) shape Depth image.
    :param model: loaded keras' h5 model with the classifier neural network
    :return: tuple(bool, string) string with the predicted image's label;
        it might be there's a part of a lamb in the image (still False).
    """
    depth_image = None
    img = None
    # We only use the depth_image right now.
    for cam in cameras:
        if cam.name == "top":
            depth_image = cam.depth_image
            break
        elif cam.name == "default" and depth_image is None:
            depth_image = cam.depth_image
        elif depth_image is None:
            img = cam.depth_image
    if depth_image is None and img is not None:
        depth_image = img
    img = None
    if depth_image is not None:
        # Crop
        img = crop_image(depth_image, 38, 102, 230, 510)
        img = filter_flies(depth_image_cropped=img)

    if img is not None:

        # predict
        img = np.array([img.reshape(230, 510, 1)])
        res = model.predict(img, verbose=0, use_multiprocessing=True)

        result_index = np.argmax(np.array(res))


        """
         Guardamos solo los frames que sean detectados como LAMB
        """
        if result_index == 0:
            print("\t CNN msg: There's a lamb. \t label:lamb")
            return True, "lamb"
        elif result_index == 1:
            print("\t CNN msg: There's no lamb. \t label:empty")
            return False, "empty"
        elif result_index == 2:
            print("\t CNN msg: There's prob. a lamb in a wrong position: \t label:wrong")
            return False, "wrong"
        else:
            print("[!] Impossible print. Something is wrong in is_there_a_lamb()")

        return True, "to_check"
    else:
        print("\t Alghtm msg: Flies detected!! \t-->\t label:fly")
        return False, "fly"



def check_changing_scene(new_frame, old_frame):
    """
    Dice si la escena del frame actual se considera distinta a la del frame anterior.
    """

    UMBRAL = 0.30 # 30%

    diff = img_diff.diff_percent_between_two_img(new_frame, old_frame)

    if diff > UMBRAL:
        return True, diff
    else:
        return False, diff
