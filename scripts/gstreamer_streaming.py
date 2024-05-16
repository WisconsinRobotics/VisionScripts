import cv2 as cv

# Camera constants
# Tested with Logitech C270 USB webcam
# Video might be crunchy, try lowering FPS or resolution for more stable streaming
FPS = 15
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Change the gstreamer pipeline as needed
GSTREAMER_PIPELINE = "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000 sync=false async=false"

# Pipeline for viewing the stream
# gst-launch-1.0 -vvv udpsrc address=127.0.0.1 port=5000 ! application/x-rtp,payload=96,encoding-name=H264 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! autovideosink sync=false -e


def main() -> None:
    cap = cv.VideoCapture(0, apiPreference=cv.CAP_V4L2)
    out = cv.VideoWriter(
        GSTREAMER_PIPELINE,
        fourcc=0,
        fps=FPS,
        frameSize=(FRAME_WIDTH, FRAME_HEIGHT),
        isColor=True,
    )

    if not cap.isOpened():
        print("Cannot open camera")
        exit(1)

    print(cap.get(cv.CAP_PROP_FOURCC))
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*"MJPG"))
    print(cap.get(cv.CAP_PROP_FOURCC))
    
    cap.set(cv.CAP_PROP_FPS, FPS)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Cannot read frame")
            break
        
        frame = cv.flip(frame, flipCode=1)
        out.write(frame)

    cap.release()


if __name__ == "__main__":
    main()
