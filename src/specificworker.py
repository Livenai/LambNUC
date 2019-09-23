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

if sys.version_info[0] < 3:
    from Model.AppState import AppState
else:
    from src.Model.AppState import AppState


# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel

class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.Period = 2000
        self.timer.start(self.Period)
        self.state = AppState()
        self.Application.start()

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
    # sm_app
    #
    @QtCore.Slot()
    def sm_app(self):
        pass

    #
    # sm_app_end
    #
    @QtCore.Slot()
    def sm_the_end(self):
        print("Entered state app_end")
        from PySide2.QtWidgets import QApplication
        QApplication.quit()

    #
    # sm_app_init
    #
    @QtCore.Slot()
    def sm_app_init(self):
        print("Entered state app_init")
        transition = self.state.starting()
        if transition is None:
            self.apptothe_end.emit()
        else:
            transition(self)

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
        pass

    #
    # sm_loading_streams
    #
    @QtCore.Slot()
    def sm_loading_streams(self):
        print("Entered state loading_streams")
        pass

    #
    # sm_getting_frames
    #
    @QtCore.Slot()
    def sm_getting_frames(self):
        print("Entered state getting_frames")
        pass

    #
    # sm_handling_events
    #
    @QtCore.Slot()
    def sm_handling_events(self):
        print("Entered state handling_events")
        pass

    #
    # sm_closing
    #
    @QtCore.Slot()
    def sm_closing(self):
        print("Entered state closing")
        pass

    #
    # sm_ask_file
    #
    @QtCore.Slot()
    def sm_ask_file(self):
        print("Entered state ask_file")
        pass

    #
    # sm_launch_window
    #
    @QtCore.Slot()
    def sm_launch_window(self):
        print("Entered state launch_window")
        pass

    #
    # sm_watch_init
    #
    @QtCore.Slot()
    def sm_watch_init(self):
        print("Entered state watch_init")
        self.state.watcher()
        self.watch_inittoget_frames.emit()

    #
    # sm_get_frames
    #
    @QtCore.Slot()
    def sm_get_frames(self):
        print("Entered state get_frames")
        transition = self.state.refresh(self.state)
        if transition is None:
            self.apptothe_end.emit()
        else:
            transition(self)

    #
    # sm_close
    #
    @QtCore.Slot()
    def sm_close(self):
        print("Entered state close")
        pass

# =================================================================
# =================================================================