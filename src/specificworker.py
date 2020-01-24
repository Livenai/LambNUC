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
#

from genericworker import *

# If RoboComp was compiled with Python bindings you can use InnerModel in Python
# sys.path.append('/opt/robocomp/lib')
# import librobocomp_qmat
# import librobocomp_osgviewer
# import librobocomp_innermodel
import os
from FileManager import save_info, FileManager, get_saved_info, url, get_weight, parent_folder
from PySide2 import QtCore
from rs_camera import RSCamera, config_devices
from lamb_filter import is_there_a_lamb
import signal
from telebot_messages import send_msg, start_bot
from keras import models
from threading import Thread

ATTEMPS_TO_STREAM = 12
ATTEMPS_TO_SAVE = 2
ATTEMPS_TO_URL = 4


class SpecificWorker(GenericWorker):
    def __init__(self, proxy_map):
        super(SpecificWorker, self).__init__(proxy_map)
        self.exit = False
        self.exceptions = [0, 0, 0] # [no_cam, no_memory, no_url]
        self.Period = 1000  # 1 second for frame

        self.timer.setInterval(self.Period)
        self.timer.setSingleShot(True)

        self.Info_period = 1000 * 60 * 60 * 8  # 8h for get an info message
        self.info_timer = QtCore.QTimer(self)
        self.info_timer.setInterval(self.Info_period)
        self.info_timer.setSingleShot(True)

        self.cameras = []
        self.lamb_label = ""
        self.weight = 0.0

        self.telegram_bot = Thread(target=start_bot)
        self.telegram_bot.start()

        self.Application.start()

        # Load the CNN model with the path to the .h5 model path
        self.CNNmodel = models.load_model(os.path.join(parent_folder, "etc", "CNN_model.h5"))

    def receive_signal(self, signum, stack):
        print("\n\n\t[eCtrl + C]\n\n")
        self.exit = True

    def __del__(self):
        print('SpecificWorker destructor')

    def setParams(self, params):
        # try:
        #	self.innermodel = InnerModel(params["InnerModelPath"])
        # except:
        #	traceback.print_exc()
        #	print("Error reading config params")
        return True

    # =============== Slots methods for State Machine ===================
    # ===================================================================
    #
    # sm_init
    #
    @QtCore.Slot()
    def sm_init(self):
        """ First state of the state machine, it triggers the LambScan main state """
        print("Entered state init")
        send_msg("LambNN initiated")
        signal.signal(signal.SIGINT, self.receive_signal)
        self.t_init_to_lambscan.emit()

    #
    # sm_lambscan
    #
    @QtCore.Slot()
    def sm_lambscan(self):
        """ The main state of the state machine, it is a sub state machine itself."""
        print("Entered state lambscan")

    #
    # sm_end
    #
    @QtCore.Slot()
    def sm_end(self):
        """ Its closes the whole application and exit of the program.
        it's the last state of the state machine. """
        print("Entered state end")
        self.Application.stop()
        from PySide2.QtWidgets import QApplication
        QApplication.quit()

    #
    # sm_start_streams
    #
    @QtCore.Slot()
    def sm_start_streams(self):
        print("Entered state start_streams")
        started = True
        try:
            self.cameras = config_devices()
            for cam in self.cameras:
                started = True if cam.start() and started else False
            if started:
                self.info_timer.start()
                if len(self.cameras) > 0:
                    self.exceptions[0] = 0
                    self.t_start_streams_to_get_frames.emit()
                else:
                    print("ERROR: There is no recognized camera connected")
                    self.exceptions[0] += 1 
                    self.t_start_streams_to_exception.emit()
            else:
                print("ERROR: It couldn't start the streams")
                self.exceptions[0] += 1
                self.t_start_streams_to_exception.emit()
        except Exception as e:
            print("problem starting the streams of the camera\n", e)
            self.exceptions[0] += 1
            self.t_start_streams_to_exception.emit()

    #
    # sm_get_frames
    #
    @QtCore.Slot()
    def sm_get_frames(self):
        print("Entered state get_frames")
        if self.exit:
            print("\n\n\t[!] Ctrl + C received. Closing program...\n\n")
            self.t_get_frames_to_exit.emit()
        self.timer.start()
        if self.info_timer.remainingTime() == 0:
            msg = ""
            for cam in self.cameras:
                msg += "  # {} camera is ready.\n".format(cam.name)
            send_msg("LambNN working with {} cams\n{}".format(len(self.cameras), msg))
            send_msg(get_saved_info())
            self.info_timer.start()
        try:
            while self.timer.remainingTime() > 0:
                for cam in self.cameras:
                    cam.get_frame()
            for cam in self.cameras:
                cam.get_frame()
            self.weight = get_weight()
            if self.weight is None:
                self.exceptions[2] += 1
                self.t_get_frames_to_exception.emit()
            else:
                self.exceptions = [0, 0, 0]
            self.t_get_frames_to_processing_and_filter.emit()
        except Exception as e:
            print("An error occur when taking a new frame,:\n " + str(e))
            print(type(e))
            self.exceptions[0] += 1
            self.t_get_frames_to_exception.emit()


    #
    # sm_exception
    #
    @QtCore.Slot()
    def sm_exception(self):
        print("Entered Exception State")
        if 0 < self.exceptions[0]:
            for cam in self.cameras:
                try:
                    del cam
                except:
                    pass
            if self.exceptions[0] >= ATTEMPS_TO_STREAM: # There's no camera
                self.t_exception_to_send_message.emit()
            else:
                self.t_exception_to_start_streams.emit()
        elif 0 < self.exceptions[1]: # There's a problem with the disk memory
            if self.no_memory > ATTEMPS_TO_SAVE:
                self.t_exception_to_send_message.emit()
            else:
                self.t_exception_to_save.emit()
        elif 0 < self.exceptions[2] < ATTEMPS_TO_URL: # There's a problem with the weight's URL
            self.t_exception_to_get_frames.emit()
        else:
            self.t_exception_to_send_message.emit()

    #
    # sm_processing_and_filter
    #
    @QtCore.Slot()
    def sm_processing_and_filter(self):
        print("Entered state Processing & Filter")
        self.no_cam = 0
        must_save, self.lamb_label = is_there_a_lamb(self.cameras, model=self.CNNmodel)
        if must_save:
            self.t_processing_and_filter_to_save.emit()
        else:
            self.t_processing_and_filter_to_get_frames.emit()

    #
    # sm_save
    #
    @QtCore.Slot()
    def sm_save(self):
        print("Entered state Save")
        try:
            save_info(self.cameras, weight=self.weight, lamb_label=self.lamb_label)
            self.lamb_label = ""
            self.weight = 0.0
            self.exceptions = [0, 0, 0]
            self.t_save_to_get_frames.emit()
        except FileManager as e:
            print(("Problem saving the file\n", e))
            self.exceptions[1] += 1
            self.t_save_to_exception.emit()

    #
    # sm_send_message
    #
    @QtCore.Slot()
    def sm_send_message(self):
        if self.exceptions == [0, 0, 0]:
            send_msg("[ ? ] Estado SEND_MESSAGE incoherente. Se ha accedido a este estado sin que haya un error.")
        else:
            send_msg("Error en LambScan, excepciones: \n {} Intentos de reconexión a la cámara. \n {} Intentos de escritura en memoria. \n {} Intentos de conexión a la URL de la báscula ({}).".format(
            *self.exceptions, url))
        self.t_send_message_to_exit.emit()

    #
    # sm_exit
    #
    @QtCore.Slot()
    def sm_exit(self):
        print("Entered state Exit")
        self.telegram_bot.do_run = False
        self.telegram_bot.join()
        for cam in self.cameras:
            try:
                del cam
            except:
                pass
        self.t_lambscan_to_end.emit()

# =================================================================
# =================================================================
