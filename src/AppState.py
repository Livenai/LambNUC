from src.rs_camera import RSCamera
from PySide2.QtCore import QTimer


class AppState:
    def __init__(self):
        self.camera = RSCamera()
        self.timer_fps = QTimer()  # Llock / Unlock GET_FRAME State
        self.timer_filter = QTimer()  # Take images without a lamb
        self.frame = (None, None)


