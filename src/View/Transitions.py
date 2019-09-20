def EXIT(self):
    if self.state.window is not None:
        self.state.window.close()
    self.startingtothe_end.emit()

def StartingW2Component(self):
    if self.state.window is not None:
        self.state.window.close()
    self.startingtocomponent.emit()


def StartingW2Watch(self):
    if self.state.window is not None:
        self.state.window.close()
    self.startingtowatch_live.emit()


def StartingW2Load(self):
    if self.state.window is not None:
        self.state.window.close()
    self.startingtoload_image.emit()


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

