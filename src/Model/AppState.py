import sys
if sys.version_info[0] < 3:
    from src.Data import RSCamera, FrameProcessor
    from src.View.GUI import *
else:
    from src.Data import RSCamera, FrameProcessor
    from src.View.GUI import WWatchLive, WStarting
import functools

STATE_COMPONENT = "COMPONENT"
STATE_LOADER = "LOAD"
STATE_WATCHER = "WATCH"

# class Borg:
#     __shared_state = {}
#
#     def __init__(self):
#         self.__dict__ = self.__shared_state





def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


# @singleton
# class TheOne:
#     pass

@singleton
class AppState:
    # __shared_state = {}

    def __init__(self):
        # self.__dict__ = self.__shared_state
        self.stopped = False
        self.image2D = True
        self.recording = 0
        self.window = None
        self.processor = None
        self.cams = []
        self.refresh = None

    def starting(self):
        # self.cams = [RSCamera()]
        # self.processor = FrameProcessor()
        #
        #
        self.window = WStarting()
        self.window.launch()

    def close(self):
        self.window.close()
        for cam in self.cams:
            cam.stop()
        self.cams = []
        self.processor

    def watcher(self):
        self.cams = [RSCamera()]
        self.processor = FrameProcessor()
        self.window = WWatchLive()
        self.window.launch()

        def get_frame(self):
            camera = self.cams[0]
            camera.start()

            while not self.window.exit:
                self.window.refresh()
                if not self.stopped:
                    color_frame, depth_frame = camera.get_frame()
                    result = processor.process(color_frame, depth_frame)
                    if self.image2D and type(result) is tuple and len(result) == 2 and processor.image2D():
                        color_image, depth_image = result
                        window.update_image(image_color=color_image, depth_image=depth_image)
                    elif not processor.image2D:
                        window.update_image(image_3D=result)
                else:
                    color_frame, depth_frame = camera.get_frame()
                    result = processor.process(color_frame, depth_frame)
                    if type(result) is tuple and len(result) == 2 and processor.image2D:
                        color_image, depth_image = result
                        window.update_image(image_color=color_image, depth_image=depth_image)
                    elif not processor.image2D:
                        window.update_image(image_3D=result)


        self.refresh = get_frame


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
