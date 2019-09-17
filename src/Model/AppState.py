from src.Data import RSCamera, FrameProcessor
from src.View.GUI import WWatchLive, WStarting

STATE_COMPONENT = "COMPONENT"
STATE_LOADER = "LOAD"
STATE_WATCHER = "WATCH"


# class Borg:
#     __shared_state = {}
#
#     def __init__(self):
#         self.__dict__ = self.__shared_state


class AppState:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.paused = True
        self.stopped = False
        self.image2D = True
        self.recording = False
        self.window = None
        self.processor = None
        self.cams = None

    def starting(self):
        # self.cams = [RSCamera()]
        # self.processor = FrameProcessor()
        #
        #
        self.window = WStarting()
        self.window.launch()

    def watcher(self):
        self.cams = [RSCamera()]
        self.processor = FrameProcessor()
        self.window = WWatchLive()

        def get_frame():
            camera.start()

            window.launch()

            while True:
                window.refresh()
                color_frame, depth_frame = camera.get_frame()
                result = processor.process(color_frame, depth_frame)
                if type(result) is tuple and len(result) == 2 and processor.is2DMode():
                    color_image, depth_image = result
                    window.update_image(image_color=color_image, depth_image=depth_image)
                elif processor.is3DMode():
                    window.update_image(image_3D=result)



def cams():
    camera = RSCamera()
    processor = FrameProcessor(camera)

    camera.start()
    color_frame, depth_frame = camera.get_frame()
    result = processor.process(color_frame, depth_frame)

    if type(result) is tuple and len(result) == 2 and processor.is2DMode():
        color_image, depth_frame = result
    elif processor.is3DMode():
        image_3D = result

    camera.stop()


if __name__ == '__main__':
    camera = RSCamera()
    processor = FrameProcessor(camera)

    window = WWatchLive()

    processor.changeMode(image3D=True)
    window.image2D = False

    camera.start()

    window.launch()

    while True:
        window.refresh()
        color_frame, depth_frame = camera.get_frame()
        result = processor.process(color_frame, depth_frame)
        if type(result) is tuple and len(result) == 2 and processor.is2DMode():
            color_image, depth_image = result
            window.update_image(image_color=color_image, depth_image=depth_image)
        elif processor.is3DMode():
            window.update_image(image_3D=result)

    camera.stop()
