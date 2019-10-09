import cv2
import numpy as np

# Constants to filter and crop the numpy images
# __edged_RGB__ = 140  # no lamb > edged > lamb
# __edged_Depth__ = 1100  # no lamb > edged > lamb

# zona de interes
Yi = 185
Xi = 14
Hi = 211
Wi = 544

# porcentaje de reduccion del mapa de voxels
voxel_scale_percent = 10

# umbral de recuento de voxels
voxel_threshold = 900  # 932 aprox.

# establecemos los umbrales
__top_threshold__ = 800
__bottom_threshold__ = 320
__under_bottom_threshold__ = 180


def isThereALamb(color_image, depth_image):
	"""
	Asks if the current image has a lamb in a right position
	:param color_image: numpy array (640, 480, 3) shape RGB image.
	:param depth_image: numpy array (640, 480, 1) shape Depth image.
	:return: tupe(bool, string) the string shows more info about the image;
		it might be there's a part of a lamb in the image (still False).
	"""
	# color_result = isLamb(color_image, depth=False)  # Old implementation
	# depth_result = isLamb(depth_image, depth=True)  # Old implementation
	# color_result = __isLamb2__(color_image) # Not used right now. It'll be used.
	depth_result = __isLamb__(depth_image)

	# TODO: hay que mejorar el algoritmo que dice si hay oveja o no.
	#  depth_result guarda ahora el numero de voxels que han superado el umbral.

	print("\tNum Voxel:\t " + str(depth_result))

	# comprobamos el numero para determinar que se ha detectado
	# if 0 <= depth_result < __under_bottom_threshold__:
	if __bottom_threshold__ <= depth_result < __top_threshold__:
		print("\tThere's a lamb")
		return True, "lamb"
	elif depth_result < __under_bottom_threshold__:
		print("\tThere's no lamb")
		return False, "no_lamb"
	elif depth_result < __bottom_threshold__:
		print("\tThere's something (prob. a lamb in a wrong position")
		return False, "error"
	elif __top_threshold__ <= depth_result:
		print("\tSomething is covering the camera")
		return False, "error"
	else:
		print("[!] Impossible print. Something is wrong in isThereALamb()")

	return True, "to_check"


# @Deprecated
# def __isLamb__(image, depth=False):
# 	"""
# 		Check if there is something in the image given by parameter
# 	:param image:
# 	:param depth:
# 	:return:
# 	"""
# 	average_left = np.mean(image[263:308, 113:208])  # crop left
# 	average_center = np.mean(image[263:308, 273:368])  # crop center
# 	average_right = np.mean(image[263:308, 413:508])  # crop right
#
# 	if depth:
# 		result = (average_left < __edged_Depth__,
# 				  average_center < __edged_Depth__, average_right < __edged_Depth__)
#
# 	else:
# 		result = (average_left > __edged_RGB__,
# 				  average_center > __edged_RGB__, average_right > __edged_RGB__)
#
# 	return result


def __isLamb__(image):
	"""
	It crops the given image in a
		Función que recorta la imagen en la zona de interes (donde se debe de encontrar la lamb)
		y reduce la imagen a un mapa de voxels. Estos voxels son la media aritmetica de
		los pixeles que abarca.
		La funcion devuelve el numero de voxels que superan el umbral de deteccion de lamb.
	:param image:
	:param depth:
	:return:
	"""
	# result = -1

	# recortamos en la zona de interes
	image_crop = image[Yi:Yi + Hi, Xi:Xi + Wi]

	# reducimos al mapa de voxels
	width = int(image_crop.shape[1] * voxel_scale_percent / 100)
	height = int(image_crop.shape[0] * voxel_scale_percent / 100)
	dim = (width, height)
	resized_image = cv2.resize(image_crop, dim, interpolation=cv2.INTER_LANCZOS4)

	return (resized_image <= voxel_threshold).sum()
	# # contamos los voxels que superan el umbral
	# for fila in resized_image:
	# 	for voxel in fila:
	# 		if voxel <= voxel_threshold:
	# 			result += 1

	# return result + 1
