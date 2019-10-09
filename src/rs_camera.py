import cv2
import pyrealsense2 as rs
import numpy as np

__HEIGHT__ = 480
__WIDTH__ = 640

#zona de interes
Yi = 185
Xi = 14
Hi = 211
Wi = 544

#porcentaje de reduccion del mapa de voxels
voxel_scale_percent = 10

#umbral derecuento de voxels
voxel_threshold = 900  # 932 aprox.

class RSCamera:
	def __init__(self):
		# Configure depth and color streams
		self.__pipeline__ = rs.pipeline()
		self.__config__ = rs.config()
		self.__config__.enable_stream(rs.stream.depth, __WIDTH__, __HEIGHT__, rs.format.z16, 30)
		self.__config__.enable_stream(rs.stream.color, __WIDTH__, __HEIGHT__, rs.format.bgr8, 30)

	# self.__config__.enable_stream(rs.stream.infrared)

	def __del__(self):
		try:
			self.stop()
		except:
			pass
		self.__pipeline__ = None
		self.__config__ = None

	def start(self):
		try:
			# Start streaming
			self.__pipeline__.start(self.__config__)
			return True
		except Exception as e:
			print(e)
			print(type(e))
			return False

	def get_frame(self):
		# Wait for a coherent pair of frames: depth and color
		frames = self.__pipeline__.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()
		if not depth_frame or not color_frame:
			return None
		depth_image = np.asanyarray(depth_frame.get_data())
		color_image = np.asanyarray(color_frame.get_data())

		return color_image, depth_image

	# Stop streaming
	def stop(self):
		self.__pipeline__.stop()

	def get_profile_intrinsics(self, profile):
		return rs.video_stream_profile(profile).get_intrinsics()

	# def pointcloud(self):
	#     return rs.pointcloud()

	def deproject_pixel_to_point(self, intrinsics, x, y, d):
		return rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], d)


# =================================================================
# =================================================================
# Constants to filter and crop the numpy images
__edged_RGB__ = 140  # no lamb > edged > lamb
__edged_Depth__ = 1100  # no lamb > edged > lamb


def isThereALamb(color_image, depth_image):
	"""
		Asks if the current image has a lamb in a right position
	:param color_image: numpy array (640, 480, 3) shape RGB image.
	:param depth_image: numpy array (640, 480, 1) shape Depth image.
	:return: tupe(bool, string) the string shows more info about the image;
		it might be there's a part of a lamb in the image (still False).
	"""
	# color_result = isLamb(color_image, depth=False)  	# Not used right now. It'll be used.
	depth_result = __isLamb2__(depth_image, depth=True)
	# if not (False in color_result or False in depth_result):
	# 	print("There's a Lamb")
	# 	return "lamb"
	# elif not (True in color_result or True in depth_result):
	# 	print("There's nothing")
	# 	return "no_lamb"
	# elif not (False in depth_result):
	# 	print("Probably a lamb")
	# 	return "probably"
	# elif not (False in color_result):
	# 	print("Check_this")
	# 	return "check"


	# -------- DEPTH --------
	'''
	if not (False in depth_result):
		print("\t\t\t\t\tdepth image: There's a Lamb")
		return True, "lamb"
	elif not (True in depth_result):
		print("\t\t\t\t\tdepth image: There's NO lamb")
		return False, "no_lamb"
	else:
		print("\t\t\t\t\tdepth image: There's something (error)")
		print("\t\t\tDepth Image detected a lamb in: ", depth_result)
		return False, "error"
	'''

	# TODO: hay que mejorar el algoritmo que dice si hay oveja o no.
	#  depth_result guarda ahora el numero de voxels que han superado el umbral.

	# establecemos los umbrales
	bad_lamb_threshold  = 180
	lamb_threshold      = 320
	over_lamb_threshold = 800

	print("\tNum Voxel:\t " + str(depth_result))

	# comprobamos el numero para determinar que se ha detectado
	if depth_result >= 0 and depth_result < bad_lamb_threshold:
		print("\tno lamb")
	elif depth_result < lamb_threshold:
		print("\tbad lamb")
	elif depth_result < over_lamb_threshold:
		print("\tlamb")
	elif depth_result >= over_lamb_threshold:
		print("\tover lamb")
	else:
		print("[!] Impossible print. Something is wrong in isThereALamb()")

	#TODO
	return True, "lamb"


def __isLamb__(image, depth=False):
	"""
		Check if there is something in the image given by parameter
	:param image:
	:param depth:
	:return:
	"""
	average_left = np.mean(image[263:308, 113:208])  # crop left
	average_center = np.mean(image[263:308, 273:368])  # crop center
	average_right = np.mean(image[263:308, 413:508])  # crop right

	if depth:
		result = (average_left < __edged_Depth__,
				  average_center < __edged_Depth__, average_right < __edged_Depth__)

	else:
		result = (average_left > __edged_RGB__,
				  average_center > __edged_RGB__, average_right > __edged_RGB__)

	return result

def __isLamb2__(image, depth=False):
	"""
		funcion que recorta la imagen en la zona de interes (donde se debe de encontrar la lamb)
		y reduce la imagen a un mapa de voxels. Estos voxels son la media aritmetica de
		los pixeles que abarca.
		La funcion devuelve el numero de voxels que superan elumbral de deteccion de lamb.
	"""
	result = -1

	#recortamos en la zona de interes
	image_crop = image[Yi:Yi+Hi, Xi:Xi+Wi]

	#reducimos al mapa de voxels
	width = int(image_crop.shape[1] * voxel_scale_percent / 100)
	height = int(image_crop.shape[0] * voxel_scale_percent / 100)
	dim = (width, height)
	resized_image = cv2.resize(image_crop, dim, interpolation=cv2.INTER_LANCZOS4)

	#cv2.imwrite(filename='/home/carlos/robocomp/components/LambSM/savings/voxel.png', img=resized_image)

	#contamos los voxels que superan el umbral
	for fila in resized_image:
		for voxel in fila:
			if voxel <= voxel_threshold:
				result += 1

	return result +1
