import cv2
import numpy as np

import customCanny

img = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)


def rate_image(edges, nr):
    # Laplace da canny extra blur nutzt  TODO - besserer weg? canny nachbauen?
    # https://github.com/FienSoP/canny_edge_detector/blob/master/canny_edge_detector.py
    # dst = cv2.Laplacian(edges, cv2.CV_8U, ksize=5)
    # # converting back to uint8
    # abs_dst = cv2.convertScaleAbs(dst)
    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    # cv2.imshow("edges", abs_dst)
    # cv2.resizeWindow('edges', 768, 1024)
    # cv2.waitKey(0)

    #abs_dst = cv2.Canny(edges, 10, 60)
    abs_dst = customCanny.Canny_detector(edges, 20, 60)

    # Gaussian 3x3    320404
    # Gaussian 5x5    284308
    # Gaussian 55x55  148884
    # Median 5x5      264633
    # Normalized 5x5  247993
    # Bilateral 5x5   291060

    # >250
    # Gaussian 3x3    4092
    # Gaussian 5x5    2487
    # Gaussian 55x55  0
    # Median 5x5      4632
    # Normalized 5x5  246
    # Bilateral 5x5   6801

    #cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
    #cv2.imshow("edges", abs_dst)
    #cv2.waitKey(0)

    # if nr == 1:
    #     cv2.imwrite("quality_img_gaus_3x3.png", abs_dst)
    # elif nr == 2:
    #     cv2.imwrite("quality_img_gaus_5x5.png", abs_dst)
    # elif nr == 3:
    #     cv2.imwrite("quality_img_gaus_55x55.png", abs_dst)
    # elif nr == 4:
    #     cv2.imwrite("quality_img_median_5x5.png", abs_dst)
    # elif nr == 5:
    #     cv2.imwrite("quality_img_norm_5x5.png", abs_dst)
    # elif nr == 6:
    #     cv2.imwrite("quality_img_bilat_5x5.png", abs_dst)

    return len(np.argwhere(abs_dst > 200))


img_gaussian_3 = cv2.GaussianBlur(img, (3, 3), 0)
img_gaussian_5 = cv2.GaussianBlur(img, (5, 5), 0)
img_gaussian_55 = cv2.GaussianBlur(img, (55, 55), 0)
img_median_5 = cv2.medianBlur(img, 5)
img_normalized_5 = cv2.blur(img, (5, 5))
img_bilateral_5 = cv2.bilateralFilter(img, 5, 5 * 2, 5 / 2)

print("Gaussian 3x3    " + str(rate_image(img_gaussian_3, 1)))
print("Gaussian 5x5    " + str(rate_image(img_gaussian_5, 2)))
print("Gaussian 55x55  " + str(rate_image(img_gaussian_55, 3)))
print("Median 5x5      " + str(rate_image(img_median_5, 4)))
print("Normalized 5x5  " + str(rate_image(img_normalized_5, 5)))
print("Bilateral 5x5   " + str(rate_image(img_bilateral_5, 6)))
cv2.destroyAllWindows()
