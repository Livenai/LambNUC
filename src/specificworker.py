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

from genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
from src.Model.AppState import AppState, STATE_COMPONENT, STATE_LOADER, STATE_WATCHER

sys.path.append('/opt/robocomp/lib')
import librobocomp_qmat
import librobocomp_osgviewer
import librobocomp_innermodel


class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 2000
        self.timer.start(self.Period)
        self.state = None

        self.global_machine.start()

    def __del__(self):
        print 'SpecificWorker destructor'

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
    # sm_starting
    #
    @QtCore.Slot()
    def sm_starting(self):
        print("Entered state starting")
        self.state = AppState()
        result = self.state.starting()
        if result == STATE_COMPONENT:
            self.startingtocomponent.emit()
        elif result == STATE_WATCHER:
            self.startingtowatch_live.emit()
        elif result == STATE_LOADER:
            self.startingtoload_image.emit()
        pass

    #
    # sm_component
    #
    @QtCore.Slot()
    def sm_component(self):
        print("Entered state component")
        pass

    #
    # sm_exception_handler
    #
    @QtCore.Slot()
    def sm_exception_handler(self):
        print("Entered state exception_handler")
        pass

    #
    # sm_load_image
    #
    @QtCore.Slot()
    def sm_load_image(self):
        print("Entered state load_image")
        pass

    #
    # sm_watch_live
    #
    @QtCore.Slot()
    def sm_watch_live(self):
        print("Entered state watch_live")
        self.state.watcher()

        self.load_streams_state.emit()

        pass

    #
    # sm_the_end
    #
    @QtCore.Slot()
    def sm_the_end(self):
        print("Entered state the_end")
        pass

    #
    # sm_load_streams
    #
    @QtCore.Slot()
    def sm_load_streams(self):
        print("Entered state load_streams")
        pass

    #
    # sm_get_frames
    #
    @QtCore.Slot()
    def sm_get_frames(self):
        print("Entered state get_frames")
        pass

    #
    # sm_save_frames
    #
    @QtCore.Slot()
    def sm_save_frames(self):
        print("Entered state save_frames")
        pass

    #
    # sm_close
    #
    @QtCore.Slot()
    def sm_close(self):
        print("Entered state close")
        pass

# =================================================================
# =================================================================
