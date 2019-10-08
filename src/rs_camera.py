import pyrealsense2 as rs
import numpy as np


class RSCamera:
	def __init__(self):
		# Configure depth and color streams
		self.__pipeline__ = rs.pipeline()
		self.__config__ = rs.config()
		self.__config__.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		self.__config__.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
		self.__profile__ = None
		self.__depth_profile__ = None
		self.__depth_intrinsics__ = None
		self.__decimate__ = rs.decimation_filter()
		self.__colorizer__ = rs.colorizer()

	def start(self):
		try:
			# Start streaming
			self.__pipeline__.start(self.__config__)

			# Get stream profile and camera intrinsics
			self.__profile__ = self.__pipeline__.get_active_profile()
			self.__depth_profile__ = rs.video_stream_profile(self.__profile__.get_stream(rs.stream.depth))

			self.__depth_intrinsics__ = self.__depth_profile__.get_intrinsics()
			w, h = self.__depth_intrinsics__.width, self.__depth_intrinsics__.height

			self.__decimate__.set_option(rs.option.filter_magnitude, 2 ** self.__decimate__)
			return True
		except Exception as e:
			print(e)
			return False

	def get_frame(self):
		try:
			# Wait for a coherent pair of frames: depth and color
			frames = self.__pipeline__.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			color_frame = frames.get_color_frame()
			if not depth_frame or not color_frame:
				return None
			depth_image = np.asanyarray(depth_frame.get_data())
			color_image = np.asanyarray(color_frame.get_data())

			return color_image, depth_image
		except Exception as e:
			print("An error occur when taking a new frame,:\n e")
			return None

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
__w_crop = 95
__h_crop = 45
__edged_RGB__ = 140  # no lamb > edged > lamb
__edged_Depth__ = 1100  # no lamb > edged > lamb
_startx = _starty = None


def isThereALamb(color_image, depth_image):
	color_result = isLamb(color_image)
	depth_result = isLamb(depth_image, depth=True)
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
	if not (False in depth_image):
		print("Lamb")
		return True, "lamb"
	elif not (True in depth_image):
		print("There's no lamb")
		return False, "no_lamb"
	else:
		print("Error")
		return False, "error"


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
