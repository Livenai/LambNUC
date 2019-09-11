import time

import cv2
import numpy as np
import pyrealsense2 as rs

from src.Data.ProcessFrame import axes, view, pointcloud, grid, frustum


class Camera:
    def __init__(self):
        # Configure depth and color streams
        self.__pipeline__ = rs.pipeline()
        self.__config__ = rs.config()
        self.__config__.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.__config__.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.__profile__ = None
        self.__depth_profile__ = None
        self.__depth_intrinsics__ = None
        self.__decimate__ = None
        self.__colorizer__ = None

    def start(self, state):
        # Start streaming
        self.__pipeline__.start(self.__config__)

        # Get stream profile and camera intrinsics
        self.__profile__ = self.__pipeline__.get_active_profile()
        self.__depth_profile__ = rs.video_stream_profile(self.__profile__.get_stream(rs.stream.depth))

        self.__depth_intrinsics__ = self.__depth_profile__.get_intrinsics()
        w, h = self.__depth_intrinsics__.width, self.__depth_intrinsics__.height

        # Processing blocks
        pc = rs.pointcloud()

        self.__decimate__ = rs.decimation_filter()
        self.__decimate__.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
        self.__colorizer__ = rs.colorizer()

    def get_frame(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.__pipeline__.wait_for_frames()
        # frames = pipeline.wait_for_frames(timeout_ms=0)

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return None
        else:
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            return color_image, depth_image

        # image_2D = True
        #
        # if image_2D:
        #     # Convert images to numpy arrays
        #     depth_image = np.asanyarray(depth_frame.get_data())
        #     color_image = np.asanyarray(color_frame.get_data())
        #
        #     return color_image, depth_image
        #
        # elif not image_2D:
        #
        #     # We need to keep the original depth_frame to save
        #     # the data; however, the visualization works better with
        #     # the depth_frame processed; so we keep both
        #     depth_frame_viewer = self.__decimate__.process(depth_frame)
        #
        #     # Grab new intrinsics (may be changed by decimation)
        #     depth_intrinsics = rs.video_stream_profile(
        #         depth_frame.profile).get_intrinsics()
        #     w, h = depth_intrinsics.width, depth_intrinsics.height
        #
        #     depth_image = np.asanyarray(depth_frame.get_data())
        #     depth_image_viewer = np.asanyarray(depth_frame_viewer.get_data())
        #     color_image = np.asanyarray(color_frame.get_data())
        #
        #     depth_colormap = np.asanyarray(
        #         self.__colorizer__.colorize(depth_frame_viewer).get_data())
        #
        #     if state.color:
        #         mapped_frame, color_source = color_frame, color_image
        #     else:
        #         mapped_frame, color_source = depth_image_viewer, depth_colormap
        #
        #     pc = rs.pointcloud()
        #     pc.map_to(mapped_frame)
        #     points = pc.calculate(depth_frame_viewer)
        #
        #     # Pointcloud data to arrays
        #     v, t = points.get_vertices(), points.get_texture_coordinates()
        #     verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        #     texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv
        #
        #     # Render
        #     now = time.time()
        #
        #     out = np.empty((h, w, 3), dtype=np.uint8)
        #
        #     out.fill(0)
        #
        #     grid(out, state, (0, 0.5, 1), size=1, n=10)
        #     frustum(out, state, depth_intrinsics)
        #     axes(out, view([0, 0, 0]), state.rotation, size=0.1, thickness=1)
        #
        #     if not state.scale or out.shape[:2] == (h, w):
        #         pointcloud(out, verts, texcoords, color_source, state)
        #     else:
        #         tmp = np.zeros((h, w, 3), dtype=np.uint8)
        #         pointcloud(tmp, verts, texcoords, color_source, state)
        #         tmp = cv2.resize(
        #             tmp, out.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
        #         np.putmask(out, tmp > 0, tmp)
        #
        #     if any(state.mouse_btns):
        #         axes(out, view(state.pivot), state.rotation, thickness=4)
        #
        #     dt = time.time() - now
        #
        #     return out

    # Stop streaming
    def stop_streaming(self, pipeline):
        self.__pipeline__.stop()
