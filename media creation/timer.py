import time

import cv2
import numpy as np

import system_info

results = [9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999]


# Index
# "gaussian_3": 0,
# "gaussian_5": 0,
# "gaussian_55": 0,
# "median_5": 0,
# "sobel_5X": 0,
# "sobel_5Y": 0,
# "Canny": 0
# TODO sobel gesamt, prewitt, andere

# list(results.items())[1][1] gets value of gaussian_3


def timer(func, pos: int, *args):
    # print(*args)
    start_time = time.perf_counter_ns()
    func(*args)
    end_time = time.perf_counter_ns() - start_time
    if end_time < results[pos]:
        results[pos] = end_time


img = cv2.imread("img.png", cv2.IMREAD_COLOR)  # FIXME sw oder bunt?
img2 = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)
i = 0
while i < 1000:
    timer(cv2.GaussianBlur, 0, img, (3, 3), 0)

    timer(cv2.GaussianBlur, 1, img, (5, 5), 0)

    timer(cv2.GaussianBlur, 2, img, (55, 55), 0)

    timer(cv2.medianBlur, 3, img, 5)

    timer(cv2.Sobel, 4, img2, cv2.CV_8U, 1, 0, 5)

    timer(cv2.Sobel, 5, img2, cv2.CV_8U, 0, 1, 5)

    timer(cv2.Canny, 6, img2, 255 / 3, 255)

    i += 1
    #print(i)

print()
print("Best Times:")
print(f'Gaussian Blur 3x3:   {results[0]} ns')
print(f"Gaussian Blur 5x5:   {results[1]} ns")
print(f"Gaussian Blur 55x55: {results[2]} ns")
print(f"Median Blur 5x5:     {results[3]} ns")
print(f"Sobel X 5x5:         {results[4]} ns")
print(f"Sobel Y 5x5:         {results[5]} ns")
print(f"Canny:               {results[6]} ns")

#system_info
