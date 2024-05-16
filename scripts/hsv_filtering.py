import cv2 as cv
import numpy as np


def main():
    img = cv.imread("sample_2.jpg")
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    cv.namedWindow("filter")

    cv.createTrackbar("low H", "filter", 0, 255, lambda a: None)
    cv.createTrackbar("high H", "filter", 0, 255, lambda a: None)
    cv.createTrackbar("low S", "filter", 0, 255, lambda a: None)
    cv.createTrackbar("high S", "filter", 0, 255, lambda a: None)
    cv.createTrackbar("low V", "filter", 0, 255, lambda a: None)
    cv.createTrackbar("high V", "filter", 0, 255, lambda a: None)

    cv.imshow("original", img)
    while True:
        if cv.waitKey(1) == ord("q"):
            break

        low_h = cv.getTrackbarPos("low H", "filter")
        high_h = cv.getTrackbarPos("high H", "filter")
        low_s = cv.getTrackbarPos("low S", "filter")
        high_s = cv.getTrackbarPos("high S", "filter")
        low_v = cv.getTrackbarPos("low V", "filter")
        high_v = cv.getTrackbarPos("high V", "filter")
        filtered_img = cv.inRange(
            hsv_img, (low_h, low_s, low_v), (high_h, high_s, high_v)
        )

        cv.imshow("filter", filtered_img)

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()


# Preliminary numbers for black:
# (60, 0, 25), (100, 80, 120)
# Preliminary numbers for white:
# (65, 10, 140), (115, 40, 255)
