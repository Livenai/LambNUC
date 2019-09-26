from src.Data import frequency, num_frames


def EXIT(self):
    self.state.close()
    self.apptothe_end.emit()


def StartingW2Component(self):
    if self.state.window is not None:
        self.state.window.close()
    self.app_inittocomponent.emit()


def StartingW2Watch(self):
    if self.state.window is not None:
        self.state.window.close()
    self.app_inittowatch_live.emit()


def StartingW2Load(self):
    if self.state.window is not None:
        self.state.window.close()
    self.app_inittoload_image.emit()


def Frame2FrameLoop(self):
    self.get_framestoget_frames.emit()


def GetFrame2SaveFrame(self):
    self.state.recording = 1
    Frame2FrameLoop(self)


def GetFrame2TakeFrames(self):
    self.state.recording = num_frames * frequency
    Frame2FrameLoop(self)


def LoadW2LoadPLY(self):
    pass


def LoadPLY2Open3D(self):
    pass


def LoadW2LoadPNGs(self):
    pass


def LoadPNGs2Open3D(self):
    pass


def LoadPNGs2Load(self):
    pass
