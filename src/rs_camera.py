import pyrealsense2 as rs
import numpy as np

__HEIGHT__ = 480
__WIDTH__ = 640


class RSCamera:
	"""
	It configures and manages the camera device (RealSense D415, D400 series) and its library (PyRealSense2).
	"""

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
		"""
		It starts the pipeline of the camera device with the default configuration.
		(Image of 640x480 shape, depth and color streams enabled)
		:return: bool: True if the starting was correct, else False.
		"""
		try:
			# Start streaming
			self.__pipeline__.start(self.__config__)
			return True
		except Exception as e:
			print(e)
			print(type(e))
			return False

	def get_frame(self):
		"""
		Get a new frame of the camera device
		:return: tupe of numpy arrays with the image
		(np.array(640x480x3) shape , np.array(640x480x1) shape) as the (color image, depth image)
		"""
		# Wait for a coherent pair of frames: depth and color
		frames = self.__pipeline__.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()
		# infrared_frame = frames.get_infrared_frame()
		if not depth_frame or not color_frame:
			return None
		depth_image = np.asanyarray(depth_frame.get_data())
		color_image = np.asanyarray(color_frame.get_data())
		# infrared_image = np.asanyarray(infrared_frame.get_data())

		return color_image, depth_image

	# return color_image, depth_image, infrared_image

	# Stop streaming
	def stop(self):
		"""
		It stops the pipeline of the camera device.
		"""
		self.__pipeline__.stop()

	def get_profile_intrinsics(self, profile):
		return rs.video_stream_profile(profile).get_intrinsics()

	def deproject_pixel_to_point(self, intrinsics, x, y, d):
		return rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], d)
