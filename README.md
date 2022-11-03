# VisionScripts

## Setup

Install gstreamer libraries:

```sh
sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
```

## Usage

Execute the RTSP Server: `python -m rtsp_server`

To view the stream, open the network stream `rtsp://<ip-address>:8554/test` in VLC.

Alternatively, run from the command line:
```sh
gst-launch-1.0 rtspsrc location=rtsp://<ip-address>:8554/test latency=100 ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720 ! autovideosink
```
