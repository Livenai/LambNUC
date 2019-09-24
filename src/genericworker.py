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

import sys, Ice, os
from PySide2 import QtWidgets, QtCore

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
	print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
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
	print 'SLICE_PATH environment variable was not exported. Using only the default paths'
	pass





class GenericWorker(QtCore.QObject):

	kill = QtCore.Signal()
#Signals for State Machine
	apptothe_end = QtCore.Signal()
	app_inittocomponent = QtCore.Signal()
	app_inittoload_image = QtCore.Signal()
	app_inittowatch_live = QtCore.Signal()
	app_inittoexception_handler = QtCore.Signal()
	componenttoapp_init = QtCore.Signal()
	componenttoexception_handler = QtCore.Signal()
	load_imagetoapp_init = QtCore.Signal()
	load_imagetoexception_handler = QtCore.Signal()
	watch_livetoapp_init = QtCore.Signal()
	watch_livetoexception_handler = QtCore.Signal()
	exception_handlertoapp_init = QtCore.Signal()
	exception_handlertocomponent = QtCore.Signal()
	exception_handlertoload_image = QtCore.Signal()
	exception_handlertowatch_live = QtCore.Signal()
	loading_streamstogetting_frames = QtCore.Signal()
	getting_framestogetting_frames = QtCore.Signal()
	getting_framestoclosing = QtCore.Signal()
	watch_inittoget_frames = QtCore.Signal()
	get_framestoget_frames = QtCore.Signal()
	get_framestoclose = QtCore.Signal()

#-------------------------

	def __init__(self, mprx):
		super(GenericWorker, self).__init__()



		
		self.mutex = QtCore.QMutex(QtCore.QMutex.Recursive)
		self.Period = 30
		self.timer = QtCore.QTimer(self)

#State Machine
		self.Application= QtCore.QStateMachine()
		self.app_state = QtCore.QState(self.Application)

		self.the_end_state = QtCore.QFinalState(self.Application)



		self.component_state = QtCore.QState(self.app_state)
		self.load_image_state = QtCore.QState(self.app_state)
		self.watch_live_state = QtCore.QState(self.app_state)
		self.exception_handler_state = QtCore.QState(self.app_state)
		self.app_init_state = QtCore.QState(self.app_state)




		self.getting_frames_state = QtCore.QState(self.component_state)
		self.loading_streams_state = QtCore.QState(self.component_state)

		self.closing_state = QtCore.QFinalState(self.component_state)



		self.get_frames_state = QtCore.QState(self.watch_live_state)
		self.watch_init_state = QtCore.QState(self.watch_live_state)

		self.close_state = QtCore.QFinalState(self.watch_live_state)


#------------------
#Initialization State machine
		self.app_state.addTransition(self.apptothe_end, self.the_end_state)
		self.app_init_state.addTransition(self.app_inittocomponent, self.component_state)
		self.app_init_state.addTransition(self.app_inittoload_image, self.load_image_state)
		self.app_init_state.addTransition(self.app_inittowatch_live, self.watch_live_state)
		self.app_init_state.addTransition(self.app_inittoexception_handler, self.exception_handler_state)
		self.component_state.addTransition(self.componenttoapp_init, self.app_init_state)
		self.component_state.addTransition(self.componenttoexception_handler, self.exception_handler_state)
		self.load_image_state.addTransition(self.load_imagetoapp_init, self.app_init_state)
		self.load_image_state.addTransition(self.load_imagetoexception_handler, self.exception_handler_state)
		self.watch_live_state.addTransition(self.watch_livetoapp_init, self.app_init_state)
		self.watch_live_state.addTransition(self.watch_livetoexception_handler, self.exception_handler_state)
		self.exception_handler_state.addTransition(self.exception_handlertoapp_init, self.app_init_state)
		self.exception_handler_state.addTransition(self.exception_handlertocomponent, self.component_state)
		self.exception_handler_state.addTransition(self.exception_handlertoload_image, self.load_image_state)
		self.exception_handler_state.addTransition(self.exception_handlertowatch_live, self.watch_live_state)
		self.loading_streams_state.addTransition(self.loading_streamstogetting_frames, self.getting_frames_state)
		self.getting_frames_state.addTransition(self.getting_framestogetting_frames, self.getting_frames_state)
		self.getting_frames_state.addTransition(self.getting_framestoclosing, self.closing_state)
		self.watch_init_state.addTransition(self.watch_inittoget_frames, self.get_frames_state)
		self.get_frames_state.addTransition(self.get_framestoget_frames, self.get_frames_state)
		self.get_frames_state.addTransition(self.get_framestoclose, self.close_state)


		self.app_state.entered.connect(self.sm_app)
		self.the_end_state.entered.connect(self.sm_the_end)
		self.app_init_state.entered.connect(self.sm_app_init)
		self.component_state.entered.connect(self.sm_component)
		self.load_image_state.entered.connect(self.sm_load_image)
		self.watch_live_state.entered.connect(self.sm_watch_live)
		self.exception_handler_state.entered.connect(self.sm_exception_handler)
		self.loading_streams_state.entered.connect(self.sm_loading_streams)
		self.closing_state.entered.connect(self.sm_closing)
		self.getting_frames_state.entered.connect(self.sm_getting_frames)
		self.watch_init_state.entered.connect(self.sm_watch_init)
		self.close_state.entered.connect(self.sm_close)
		self.get_frames_state.entered.connect(self.sm_get_frames)

		self.Application.setInitialState(self.app_state)
		self.app_state.setInitialState(self.app_init_state)
		self.component_state.setInitialState(self.loading_streams_state)
		self.watch_live_state.setInitialState(self.watch_init_state)

#------------------

#Slots funtion State Machine
	@QtCore.Slot()
	def sm_n(self):
		print "Error: lack sm_n in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_o(self):
		print "Error: lack sm_o in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_n(self):
		print "Error: lack sm_n in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_e(self):
		print "Error: lack sm_e in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_app(self):
		print "Error: lack sm_app in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_the_end(self):
		print "Error: lack sm_the_end in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_component(self):
		print "Error: lack sm_component in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_load_image(self):
		print "Error: lack sm_load_image in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_watch_live(self):
		print "Error: lack sm_watch_live in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_exception_handler(self):
		print "Error: lack sm_exception_handler in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_app_init(self):
		print "Error: lack sm_app_init in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_getting_frames(self):
		print "Error: lack sm_getting_frames in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_loading_streams(self):
		print "Error: lack sm_loading_streams in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_closing(self):
		print "Error: lack sm_closing in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_get_frames(self):
		print "Error: lack sm_get_frames in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_watch_init(self):
		print "Error: lack sm_watch_init in Specificworker"
		sys.exit(-1)

	@QtCore.Slot()
	def sm_close(self):
		print "Error: lack sm_close in Specificworker"
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
		print "Period changed", p
		Period = p
		timer.start(Period)
