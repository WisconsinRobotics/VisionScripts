import cv2 as cv
import numpy as np
from util import *


def main(filename: str = "sample.jpg"):
    img = cv.imread(filename)
    cv.imshow("original img", img)

    img_mask_black = mask_black(img)
    cv.imshow("black threshold", img_mask_black)

    img_mask_white = mask_white(img)
    cv.imshow("white threshold", img_mask_white)

    img_masks_combined = combine_masks(img_mask_black, img_mask_white)
    cv.imshow("combine masks", img_masks_combined)

    contour_img = img.copy()
    contours = find_contours(img_masks_combined)
    cv.drawContours(contour_img, contours, -1, (0, 0, 255), 2)
    cv.imshow("contours", contour_img)

    aruco_img = img.copy()
    (corners, ids, _) = detect_aruco(img)
    cv.aruco.drawDetectedMarkers(aruco_img, corners, ids)

    side_lengths = []
    for i in range(len(corners[0][0])):
        side_lengths.append(np.linalg.norm(corners[0][0][i - 1] - corners[0][0][i]))

    print(side_lengths, sum(side_lengths) / 4, (sum(side_lengths) / 4) ** 2)
    area_estimate = max(side_lengths) ** 2

    distance_estimate = SIDE_LENGTH_1FT / max(side_lengths)
    print(area_estimate, distance_estimate)

    cv.imshow("aruco module", aruco_img)

    cv.waitKey()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
