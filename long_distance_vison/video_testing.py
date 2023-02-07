import time

import cv2 as cv
from util import *


def main():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print('Cannot open camera')
        exit(1)

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print('Cannot read frame')
            break

        cv.imshow('frame', frame)
    
        # img_mask_black = mask_black(frame)
        # cv.imshow('black threshold', img_mask_black)
        # img_mask_white = mask_white(frame)
        # cv.imshow('white threshold', img_mask_white)
        # img_masks_combined = combine_masks(img_mask_black, img_mask_white)
        # cv.imshow('combine masks', img_masks_combined)

        contour_frame = frame.copy()
        cv.drawContours(contour_frame, get_aruco_contours(contour_frame), -1, (0,0,255), 2)
        cv.imshow('contour frame', contour_frame)

        aruco_frame = frame.copy()
        (corners, ids, _) = detect_aruco(aruco_frame)
        cv.aruco.drawDetectedMarkers(aruco_frame, corners, ids)
        cv.imshow('aruco frame', aruco_frame)

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
             cv.imwrite('webcam-' + time.strftime("%Y%m%d_%H%M%S") + ".jpg", frame)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
