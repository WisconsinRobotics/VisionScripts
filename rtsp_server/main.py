#!/usr/bin/env python3

import argparse
import gi
# import cv2 as cv

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject


class CameraMediaFactory(GstRtspServer.RTSPMediaFactory):
    """
    RTSPMediaFactory containing a v4l2src camera pipeline.
    """
    def __init__(self, width, height, **kwargs):
        super().__init__()
        # src = f'videotestsrc ! video/x-raw,rate=30,width={width},height={height},format=I420'
        src = f'v4l2src ! image/jpeg,rate=30,width={width},height={height} ! decodebin ! videoconvert ! video/x-raw,format=I420 ! videoconvert' 
        h264 = 'x264enc speed-preset=ultrafast tune=zerolatency'
        self.pipeline_str = f'{src} ! {h264} ! rtph264pay config-interval=1 name=pay0 pt=96'
    
    def do_create_element(self, url):
        return Gst.parse_launch(self.pipeline_str)


class CVMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super.__init__()
        # TODO define pipeline with OpenCV


class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self, port, **kwargs):
        super().__init__()
        self.factory = CameraMediaFactory(**kwargs)
        self.factory.set_shared(True)
        self.set_service(str(port))
        self.get_mount_points().add_factory('/test', self.factory)
        self.attach(None)
        

def main(args=None):
    parser = argparse.ArgumentParser()
    # parser.add_argument('--device_id', required=True, type=int)
    parser.add_argument('--width', default=1280, type=int)
    parser.add_argument('--height', default=720, type=int)
    parser.add_argument('--port', default=8554, type=int)
    args = parser.parse_args(args)
    args_dict = vars(args)

    GObject.threads_init()
    Gst.init(None)
    server = RTSPServer(**args_dict)
    loop = GObject.MainLoop()
    loop.run()
