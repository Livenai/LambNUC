import cv2
import numpy as np

# zona de interes
Yi = 185
Xi = 14
Hi = 211
Wi = 544

# porcentaje de reduccion del mapa de voxels
voxel_scale_percent = 10

# umbral de recuento de voxels
voxel_threshold = 1000  # 932 aprox.

# establecemos los umbrales
__top_threshold__ = 800
__bottom_threshold__ = 430
__under_bottom_threshold__ = 100


def isThereALamb(color_image, depth_image):
	"""
	Asks if the current image has a lamb in a right position
	:param color_image: numpy array (640, 480, 3) shape RGB image.
	:param depth_image: numpy array (640, 480, 1) shape Depth image.
	:return: tupe(bool, string) the string shows more info about the image;
		it might be there's a part of a lamb in the image (still False).
	"""
	depth_result = __isLamb__(depth_image)
	# print("\tNum Voxel:\t " + str(depth_result))

	# comprobamos el numero para determinar que se ha detectado
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


def __isLamb__(image):
	"""
	Función que recorta la imagen en la zona de interes (donde se debe de encontrar la lamb)
	y reduce la imagen a un mapa de voxels. Estos voxels son la media aritmetica de
	los pixeles que abarca.
	La funcion devuelve el numero de voxels que superan el umbral de deteccion de lamb.
	:param image: numpy array with (640x480x1) shape (in case of depth image, which is the case;
	but it could be (640x480x3) of shape if we use a color image).
	:return: int with the sumatory of the voxels which satisfied the detection condition.
	"""
	# recortamos en la zona de interes
	image_crop = image[Yi:Yi + Hi, Xi:Xi + Wi]

	# reducimos al mapa de voxels
	width = int(image_crop.shape[1] * voxel_scale_percent / 100)
	height = int(image_crop.shape[0] * voxel_scale_percent / 100)
	dim = (width, height)
	resized_image = cv2.resize(image_crop, dim, interpolation=cv2.INTER_LANCZOS4)

	# return (resized_image <= voxel_threshold).sum()
	return np.count_nonzero(resized_image <= voxel_threshold)
