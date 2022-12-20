from math import sqrt

import cv2
import numpy as np


# Erstellen von Abbildungen für den schriftlichen Teil


def blur_image():
    img = cv2.imread("img.png", cv2.IMREAD_COLOR)

    img_blured_3 = cv2.GaussianBlur(img, (25, 25), 0)
    cv2.imwrite('blured_img_25x25.png', img_blured_3)

    img_blured_5 = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imwrite('blured_img_5x5.png', img_blured_5)

    img_blured_55 = cv2.GaussianBlur(img, (55, 55), 0)
    cv2.imwrite('blured_img_55x55.png', img_blured_55)

    img_blured_median = cv2.medianBlur(img, ksize=25)
    cv2.imwrite('blured_img_median_25x25.png', img_blured_median)

    img_blured_norm = cv2.blur(img, (25, 25))
    cv2.imwrite('blured_img_blur_25x25.png', img_blured_norm)

    img_blured_bilat = cv2.bilateralFilter(img, 25, 5 * 2, 5 / 2)
    cv2.imwrite('blured_img_bilat_25x2.png', img_blured_bilat)


def edges():
    img = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)

    cv2.imwrite('img_grey.png', img)

    # Prewitt

    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    img_prewittx = cv2.filter2D(img, -1, kernelx)
    img_prewitty = cv2.filter2D(img, -1, kernely)

    cv2.imwrite('edge_img_prewittX.png', img_prewittx)
    cv2.imwrite('edge_img_prewittY.png', img_prewitty)

    # Sobel

    img_sobelx = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=5)
    img_sobely = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=5)
    #img_sobel_gesamt = np.sqrt(img_sobelx**2 + img_sobely**2)

    img_sobel_gesamt = cv2.addWeighted(img_sobelx, 0.5, img_sobely, 0.5 , 0.0)

    cv2.imwrite('edge_img_sobelX.png', img_sobelx)
    cv2.imwrite('edge_img_sobelY.png', img_sobely)
    cv2.imwrite('edge_img_sobelGESAMT.png', img_sobel_gesamt)

    # Canny

    img_canny = cv2.Canny(img, 50, 150)  # obere/untere Grenze 255/3 255

    cv2.imwrite('edge_img_canny.png', img_canny)

    # TODO more Laplace?


if __name__ == '__main__':
    #blur_image()
    edges()
