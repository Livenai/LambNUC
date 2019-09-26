import numpy as np

# TODO : determines an appropiate number (or let it be stablished by a configuration file)
__w_crop = 95
__h_crop = 45
__edged_RGB__ = 140
# rgb
# with lamb:
# 167
# 183
# 197
# with no lamb:
# 41
# 35
# 51


__edged_Depth__ = 1100  # no lamb > average > lamb


# depth
# with lamb:
# 963
# 962
# 899
# 904
# 1044
# 1042

# no_lamb:
# 1295
# 1379
# 1453


def filterColor(color_image):
    pass


def filterDepth(depth_image):
    pass


def cropImage(image):
    pass


def mustSave(color_image, depth_image):
    return True


def isThereALamb(color_image, depth_image):
    color_result = isLamb(color_image)
    depth_result = isLamb(depth_image)
    if not (False in color_result or False in depth_result):
        print "There's a Lamb"
    elif not (True in color_result or True in depth_result):
        print "There's nothing"
    elif False not in depth_result:
        print "Probably a lamb"
    elif False not in color_result:
        print "Check_this"
    else:
        print "Error"


def isLamb(image, depth=False):
    conf = (image, __w_crop, __h_crop, depth)
    average_left = np.mean(__crop_left__(*conf))
    average_center = np.mean(__crop_center__(*conf))
    average_right = np.mean(__crop_right__(*conf))

    if depth:
        result = (average_left < __edged_Depth__,
                  average_center < __edged_Depth__, average_right < __edged_Depth__)

    else:
        result = (average_left > __edged_RGB__,
                  average_center > __edged_RGB__, average_right > __edged_RGB__)

    return result


_startx = _starty = None


def __crop__(img, cropx, cropy, depth):
    global _startx, _starty
    if depth:
        y, x = img.shape
    else:
        y, x, _ = img.shape
    _startx = x // 2 - (cropx // 2)
    _starty = y // 2 - (cropy // 2) + 45
    return _startx, _starty


def __crop_center__(img, cropx, cropy, depth=False):
    if _startx is None or _starty is None:
        startx, starty = __crop__(img, cropx, cropy, depth)
    return img[_starty:_starty + cropy, _startx:_startx + cropx]


def __crop_left__(img, cropx, cropy, depth=False):
    if _startx is None or _starty is None:
        startx, starty = __crop__(img, cropx, cropy, depth)
    else:
        startx, starty = _startx, _starty
    startx -= 160
    return img[starty:starty + cropy, startx:startx + cropx]


def __crop_right__(img, cropx, cropy, depth=False):
    if _startx is None or _starty is None:
        startx, starty = __crop__(img, cropx, cropy, depth)
    else:
        startx, starty = _startx, _starty
    startx += 140
    return img[starty:starty + cropy, startx:startx + cropx]
