#!/usr/bin/python3
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

import sys, Ice, os
from PySide2 import QtWidgets, QtCore

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
	print('$ROBOCOMP environment variable not set, using the default value /opt/robocomp')
	ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior

additionalPathStr = ''
icePaths = [ '/opt/robocomp/interfaces' ]
try:
	SLICE_PATH = os.environ['SLICE_PATH'].split(':')
	for p in SLICE_PATH:
		icePaths.append(p)
		additionalPathStr += ' -I' + p + ' '
	icePaths.append('/opt/robocomp/interfaces')
except:
	print('SLICE_PATH environment variable was not exported. Using only the default paths')
	pass





class GenericWorker(QtCore.QObject):

	kill = QtCore.Signal()
#Signals for State Machine
	t_init_to_lambscan = QtCore.Signal()
	t_lambscan_to_end = QtCore.Signal()
	t_start_streams_to_get_frames = QtCore.Signal()
	t_start_streams_to_no_camera = QtCore.Signal()
	t_start_streams_to_send_message = QtCore.Signal()
	t_get_frames_to_processing_and_filter = QtCore.Signal()
	t_get_frames_to_no_camera = QtCore.Signal()
	t_get_frames_to_get_frames = QtCore.Signal()
	t_get_frames_to_exit = QtCore.Signal()
	t_processing_and_filter_to_get_frames = QtCore.Signal()
	t_processing_and_filter_to_save = QtCore.Signal()
	t_save_to_get_frames = QtCore.Signal()
	t_save_to_no_memory = QtCore.Signal()
	t_no_camera_to_start_streams = QtCore.Signal()
	t_no_camera_to_send_message = QtCore.Signal()
	t_no_memory_to_save = QtCore.Signal()
	t_no_memory_to_send_message = QtCore.Signal()
	t_send_message_to_exit = QtCore.Signal()

#-------------------------

	def __init__(self, mprx):
		super(GenericWorker, self).__init__()



		
		self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
		self.Period = 30
		self.timer = QtCore.QTimer(self)

#State Machine
		self.Application= QtCore.QStateMachine()
		self.lambscan_state = QtCore.QState(self.Application)
		self.init_state = QtCore.QState(self.Application)

		self.end_state = QtCore.QFinalState(self.Application)



		self.get_frames_state = QtCore.QState(self.lambscan_state)
		self.processing_and_filter_state = QtCore.QState(self.lambscan_state)
		self.save_state = QtCore.QState(self.lambscan_state)
		self.no_camera_state = QtCore.QState(self.lambscan_state)
		self.no_memory_state = QtCore.QState(self.lambscan_state)
		self.send_message_state = QtCore.QState(self.lambscan_state)
		self.start_streams_state = QtCore.QState(self.lambscan_state)

		self.exit_state = QtCore.QFinalState(self.lambscan_state)


#------------------
#Initialization State machine
		self.init_state.addTransition(self.t_init_to_lambscan, self.lambscan_state)
		self.lambscan_state.addTransition(self.t_lambscan_to_end, self.end_state)
		self.start_streams_state.addTransition(self.t_start_streams_to_get_frames, self.get_frames_state)
		self.start_streams_state.addTransition(self.t_start_streams_to_no_camera, self.no_camera_state)
		self.start_streams_state.addTransition(self.t_start_streams_to_send_message, self.send_message_state)
		self.get_frames_state.addTransition(self.t_get_frames_to_processing_and_filter, self.processing_and_filter_state)
		self.get_frames_state.addTransition(self.t_get_frames_to_no_camera, self.no_camera_state)
		self.get_frames_state.addTransition(self.t_get_frames_to_get_frames, self.get_frames_state)
		self.get_frames_state.addTransition(self.t_get_frames_to_exit, self.exit_state)
		self.processing_and_filter_state.addTransition(self.t_processing_and_filter_to_get_frames, self.get_frames_state)
		self.processing_and_filter_state.addTransition(self.t_processing_and_filter_to_save, self.save_state)
		self.save_state.addTransition(self.t_save_to_get_frames, self.get_frames_state)
		self.save_state.addTransition(self.t_save_to_no_memory, self.no_memory_state)
		self.no_camera_state.addTransition(self.t_no_camera_to_start_streams, self.start_streams_state)
		self.no_camera_state.addTransition(self.t_no_camera_to_send_message, self.send_message_state)
		self.no_memory_state.addTransition(self.t_no_memory_to_save, self.save_state)
		self.no_memory_state.addTransition(self.t_no_memory_to_send_message, self.send_message_state)
		self.send_message_state.addTransition(self.t_send_message_to_exit, self.exit_state)


		self.lambscan_state.entered.connect(self.sm_lambscan)
		self.init_state.entered.connect(self.sm_init)
		self.end_state.entered.connect(self.sm_end)
		self.start_streams_state.entered.connect(self.sm_start_streams)
		self.exit_state.entered.connect(self.sm_exit)
		self.get_frames_state.entered.connect(self.sm_get_frames)
		self.processing_and_filter_state.entered.connect(self.sm_processing_and_filter)
		self.save_state.entered.connect(self.sm_save)
		self.no_camera_state.entered.connect(self.sm_no_camera)
		self.no_memory_state.entered.connect(self.sm_no_memory)
		self.send_message_state.entered.connect(self.sm_send_message)

		self.Application.setInitialState(self.init_state)
		self.lambscan_state.setInitialState(self.start_streams_state)

#------------------

#Slots funtion State Machine
	@QtCore.Slot()
	def sm_lambscan(self):
		print("Error: lack sm_lambscan in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_init(self):
		print("Error: lack sm_init in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_end(self):
		print("Error: lack sm_end in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_get_frames(self):
		print("Error: lack sm_get_frames in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_processing_and_filter(self):
		print("Error: lack sm_processing_and_filter in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_save(self):
		print("Error: lack sm_save in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_no_camera(self):
		print("Error: lack sm_no_camera in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_no_memory(self):
		print("Error: lack sm_no_memory in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_send_message(self):
		print("Error: lack sm_send_message in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_start_streams(self):
		print("Error: lack sm_start_streams in Specificworker")
		sys.exit(-1)

	@QtCore.Slot()
	def sm_exit(self):
		print("Error: lack sm_exit in Specificworker")
		sys.exit(-1)


#-------------------------
	@QtCore.Slot()
	def killYourSelf(self):
		rDebug("Killing myself")
		self.kill.emit()

	# \brief Change compute period
	# @param per Period in ms
	@QtCore.Slot(int)
	def setPeriod(self, p):
		print("Period changed", p)
		self.Period = p
		self.timer.start(self.Period)
