import pyrealsense2 as rs
import numpy as np

__HEIGHT__ = 480
__WIDTH__ = 640


class RSCamera:
	def __init__(self):
		# Configure depth and color streams
		self.__pipeline__ = rs.pipeline()
		self.__config__ = rs.config()
		self.__config__.enable_stream(rs.stream.depth, __WIDTH__, __HEIGHT__, rs.format.z16, 30)
		self.__config__.enable_stream(rs.stream.color, __WIDTH__, __HEIGHT__, rs.format.bgr8, 30)
		# self.__config__.enable_stream(rs.stream.infrared)

		# self.__profile__ = None
		# self.__depth_profile__ = None
		# self.__depth_intrinsics__ = None
		# self.__decimate__ = None
		# self.__colorizer__ = None

	def __del__(self):
		try:
			self.stop()
		except:
			pass

		self.__pipeline__ = None
		self.__config__ = None
		# self.__profile__ = None
		# self.__depth_profile__ = None
		# self.__depth_intrinsics__ = None
		# self.__decimate__ = None
		# self.__colorizer__ = None

	def start(self):
		try:
			# Start streaming
			self.__pipeline__.start(self.__config__)
			# self.__decimate__ = rs.decimation_filter()
			# self.__colorizer__ = rs.colorizer()
			#
			# # Get stream profile and camera intrinsics
			# self.__profile__ = self.__pipeline__.get_active_profile()
			# self.__depth_profile__ = rs.video_stream_profile(self.__profile__.get_stream(rs.stream.depth))
			#
			# self.__depth_intrinsics__ = self.__depth_profile__.get_intrinsics()
			# self.__decimate__.set_option(rs.option.filter_magnitude, 2 ** self.__decimate__)
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
	# color_result = isLamb(color_image)  	# Not used right now. It'll be used.
	depth_result = __isLamb__(depth_image, depth=True)
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

	# TODO: hay que mejorar el algoritmo que dice si hay oveja o no.
	# De momento el codigo esta preparado
	# para mostrar por pantalla si se detecta oveja o no, tanto en la imagen RGB como en la imagen de
	# profundidad.
	# Una vez mejorado, se puede modificar el codigo de esta funcion para que retorne los datos debidamente.

	# -------- DEPTH --------
	if not (False in depth_result):
		print("\t\t\t\t\tdepth: Lamb")
		return True, "lamb"
	elif not (True in depth_result):
		print("\t\t\t\t\tdepth: NO lamb")
		return False, "no_lamb"
	else:
		print("\t\t\t\t\tdepth: Error")
		return False, "error"


def __isLamb__(image, depth=False):
	"""
		Check if there is something in the image given by parameter
	:param image:
	:param depth:
	:return:
	"""
	# conf = (image, __w_crop, __h_crop, depth)
	average_left = np.mean(image[263:308, 113:208])
	average_center = np.mean(image[263:308, 273:368])
	average_right = np.mean(image[263:308, 413:508])  # crop right

	if depth:
		result = (average_left < __edged_Depth__,
				  average_center < __edged_Depth__, average_right < __edged_Depth__)

	else:
		result = (average_left > __edged_RGB__,
				  average_center > __edged_RGB__, average_right > __edged_RGB__)

	return result

# def __crop__(img, cropx, cropy, depth):
# 	global _startx, _starty
# 	if depth:
# 		y, x = img.shape
# 	else:
# 		y, x, _ = img.shape
# 	_startx = x // 2 - (cropx // 2)
# 	_starty = y // 2 - (cropy // 2) + 45
# 	return _startx, _starty
#
#
# def __crop_center__(img, cropx, cropy, depth=False):
# 	# return img[263:308, 273:368]
# 	if _startx is None or _starty is None:
# 		startx, starty = __crop__(img, cropx, cropy, depth)
# 	return img[_starty:_starty + cropy, _startx:_startx + cropx]
#
#
# def __crop_left__(img, cropx, cropy, depth=False):
# 	# return img[263:308, 113:208]
# 	if _startx is None or _starty is None:
# 		startx, starty = __crop__(img, cropx, cropy, depth)
# 	else:
# 		startx, starty = _startx, _starty
# 	startx -= 160
# 	return img[starty:starty + cropy, startx:startx + cropx]
#
#
# def __crop_right__(img, cropx, cropy, depth=False):
# 	# return img[263:308, 413:508] # crop right
# 	if _startx is None or _starty is None:
# 		startx, starty = __crop__(img, cropx, cropy, depth)
# 	else:
# 		startx, starty = _startx, _starty
# 	startx += 140
# 	return img[starty:starty + cropy, startx:startx + cropx]


# if __name__ == '__main__':
# 	import cv2
#
# 	filename = "/home/alberto/Documents/LambSM/savings/color/lamb/2019-10-04/2019-10-04 11:37:56.660649_cam01_color.png"
# 	image_color = cv2.imread(filename)
# 	filename.replace("color", "depth")
# 	image_depth = cv2.imread(filename)
# 	isLamb(image_color, depth=False)
# 	isLamb(image_depth, depth=True)
