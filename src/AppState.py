from src.rs_camera import RSCamera


class AppState:
    def __init__(self):
        self.camera = RSCamera()
        self.frame = (None, None)
        self.start = self.camera.start

    def get_frame(self):
        self.frame = self.camera.get_frame()
        return self.frame
