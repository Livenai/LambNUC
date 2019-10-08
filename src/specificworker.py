#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#


# from genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
from src.AppState import AppState
from src.FileManager import save_frames
from src.genericworker import GenericWorker
from PySide2 import QtCore

from src.rs_camera import isThereALamb


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.no_cam = 0
		self.no_memory = 0
		self.Period = 1000  # 1 second for frame
		# self.timer.timeout.connect(self.t_get_frames_to_processing_and_filter.emit)
		# self.timer.start(self.Period)
		self.Saver_period = 1000 * 60 * 25  # 25 min for a random picture
		self.saver_timer = QtCore.QTimer(self)

		self.state = None
		self.Application.start()

	def __del__(self):
		print('SpecificWorker destructor')

	def setParams(self, params):
		# try:
		#	self.innermodel = InnerModel(params["InnerModelPath"])
		# except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True

	# =============== Slots methods for State Machine ===================
	# ===================================================================
	#
	# sm_init
	#
	@QtCore.Slot()
	def sm_init(self):
		print("Entered state init")
		self.state = AppState()
		self.t_init_to_lambscan.emit()

	#
	# sm_lambscan
	#
	@QtCore.Slot()
	def sm_lambscan(self):
		print("Entered state lambscan")

	# self.t_lambscan_to_end.emit()

	#
	# sm_end
	#
	@QtCore.Slot()
	def sm_end(self):
		print("Entered state end")
		self.Application.quit()
		pass

	#
	# sm_start_streams
	#
	@QtCore.Slot()
	def sm_start_streams(self):
		print("Entered state start_streams")
		try:
			self.state.start()
			self.t_start_streams_to_get_frames.emit()
		except Exception as e:
			print("problem starting the streams of the camera")
			print(e)
			self.t_start_streams_to_no_camera.emit()

	#
	# sm_get_frames
	#
	@QtCore.Slot()
	def sm_get_frames(self):
		print("Entered state get_frames")
		# TODO.
		self.timer.setInterval(self.Period)
		self.timer.timeout.connect(self.t_get_frames_to_get_frames.emit)
		self.timer.singleShot()
		try:
			while self.timer.remainingTime() > 0:
				self.state.get_frame()
			self.t_get_frames_to_processing_and_filter.emit()
		except Exception as e:
			print("Error taking the frame\n", e)
			self.t_get_frames_to_no_camera.emit()

	#
	# sm_no_camera
	#
	@QtCore.Slot()
	def sm_no_camera(self):
		print("Entered state no_camera")
		self.no_cam += 1
		if self.no_cam > 12:
			self.t_no_camera_to_send_message.emit()
		else:
			self.t_no_camera_to_start_streams.emit()

	#
	# sm_no_memory
	#
	@QtCore.Slot()
	def sm_no_memory(self):
		print("Entered state no_memory")
		self.no_memory += 1
		if self.no_memory > 2:
			self.t_no_memory_to_send_message.emit()
		else:
			self.t_no_memory_to_save.emit()

	#
	# sm_processing_and_filter
	#
	@QtCore.Slot()
	def sm_processing_and_filter(self):
		print("Entered state processing_and_filter")
		lamb, path_name = isThereALamb(*self.state.frame)
		self.state.lamb_path = path_name
		if lamb:
			self.t_processing_and_filter_to_save.emit()
		else:
			# TODO.
			# self.saver_timer.setInterval(self.Saver_period)
			# self.saver_timer.timeout.connect(self.t_get_frames_to_get_frames.emit)
			# self.saver_timer.singleShot()
			# while self.saver_timer.remainingTime() > 0:
			# 	self.t_processing_and_filter_to_save.emit()
			# self.t_get_frames_to_processing_and_filter.emit()

			if self.saver_timer.remainingTime() > 1:
				self.t_processing_and_filter_to_save.emit()

	#
	# sm_save
	#
	@QtCore.Slot()
	def sm_save(self):
		print("Entered state save")
		try:
			save_frames(*self.state.frame, self.state.lamb_path)
		# TODO.
		# self.saver_timer.setInterval(self.Saver_period)
		# self.saver_timer.timeout.connect(self.t_get_frames_to_get_frames.emit)
		# self.saver_timer.singleShot()
		except Exception as e:
			print("Problem saving the file", e)
			self.t_save_to_no_memory.emit()

	#
	# sm_send_message
	#
	@QtCore.Slot()
	def sm_send_message(self):
		print("Entered state send_message")
		print("- Not implemented yet, send an email to the developers.")
		self.t_send_message_to_exit.emit()

	#
	# sm_exit
	#
	@QtCore.Slot()
	def sm_exit(self):
		print("Entered state exit")
		self.t_lambscan_to_end.emit()

# =================================================================
# =================================================================
