import cv2 as cv
import numpy as np


def mask_black(img: np.ndarray):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # black_thresh = cv.inRange(hsv, (0, 0, 0), (180, 255, 120))
    black_thresh = cv.inRange(hsv, (60, 0, 25), (100, 80, 120))
    return black_thresh


def mask_white(img: np.ndarray):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    white_thresh = cv.inRange(hsv, (65, 10, 140), (115, 40, 255))
    return white_thresh


def combine_masks(mask_a: np.ndarray, mask_b: np.ndarray, kernel_size: int=7):
    kernel = np.ones((kernel_size, kernel_size), np.int8)
    mask_a_convolution = cv.filter2D(mask_a, -1, kernel)
    mask_b_convolution = cv.filter2D(mask_b, -1, kernel)
    and_convolutions = cv.bitwise_and(mask_a_convolution, mask_b_convolution)
    return and_convolutions


def gaussian_blur_discrete(img: np.ndarray, kernel_size: int=5):
    blur = cv.GaussianBlur(img, (kernel_size, kernel_size), 20)
    discrete_blur = cv.inRange(blur, 1, 255)
    return discrete_blur


def find_contours(img_mask: np.ndarray):
    contours, hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    rectangular_contours = []
    for contour in contours:
        # TODO make epsilon here not a magic number
        approx = cv.approxPolyDP(contour, 2.5, True)
        if len(approx) == 4:
            rectangular_contours.append(approx)

    return rectangular_contours


def main(filename: str='sample_1.jpg'):
    img = cv.imread(filename)
    cv.imshow('original img', img)

    img_mask_black = mask_black(img)
    cv.imshow('black threshold', img_mask_black)

    img_mask_white = mask_white(img)
    cv.imshow('white threshold', img_mask_white)

    img_masks_combined = combine_masks(img_mask_black, img_mask_white)
    cv.imshow('combine masks', img_masks_combined)

    contours = find_contours(img_masks_combined)
    contour_img = cv.drawContours(img, contours, -1, (0,0,255), 2)
    cv.imshow('contours', contour_img)

    cv.waitKey()
    cv.destroyAllWindows


if __name__ == '__main__':
    main()
