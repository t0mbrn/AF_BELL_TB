import time

# import system_info #FIXME wird hier angezeigt
import cv2
import numpy
import numpy as np

print("Comparison: Performance of AF Components")

# results = [9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999, 9999999999999]
results = [[3263800, 956600],  # 0 "gaussian_3"
           [3500900, 1030100],  # 1 "gaussian_5"
           [34646300, 13751600],  # 2 "gaussian_55"
           [21784000, 10911400],  # 3 "median_5"
           [13730600, 4512700],
           # 4 "normalized blur_5" ------ https://stackoverflow.com/questions/34139971/opencv-homogeneus-blur-slower-than-gaussian-blur
           [17550300, 21607600],  # 5 "bilateral blur_5" #
           [0, 2225100],  # 6 "sobel_5X"
           [0, 2183400],  # 7 "sobel_5Y" but with ksize instead of (5,5) ?
           [0, 60258700],  # 8 "sobel ges 5"
           [0, 7880300],  # 9 "Canny"
           [0, 5482000]]  # 10 laplace

# results = [[3263800, 9999999999999],  # 0 "gaussian_3"
#            [3500900, 9999999999999],  # 1 "gaussian_5"
#            [34646300, 9999999999999],  # 2 "gaussian_55"
#            [21784000, 9999999999999],  # 3 "median_5"
#            [9999999999999, 9999999999999],  # 4 "normalized blur_5"
#            [9999999999999, 9999999999999],  # 5 "bilateral blur_5"
#            [0, 3261800],  # 4 "sobel_5X"
#            [0, 3188900],  # 5 "sobel_5Y"
#            [0, 9999999999999],  # 9 "sobel ges 5" - vereinfacht 8016300
#            [0, 7880300]]  # 6 "Canny"

# Index 0: bunt, 1: sw

# TODO prewitt, laplace andere

img = cv2.imread("img.png", cv2.IMREAD_COLOR)  # FIXME sw oder bunt?
img2 = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)

buffer = 60  # sec


def timer(func, pos1: int, pos2: int, *args, **kwargs):
    initial_time = time.time()

    while time.time() < (initial_time + buffer):
        # print(*args)
        start_time = time.perf_counter_ns()
        func(*args, **kwargs)
        end_time = time.perf_counter_ns() - start_time
        if end_time < results[pos1][pos2]:
            results[pos1][pos2] = end_time
            initial_time = time.time()


def sobel_edge_detector():  # https://stackoverflow.com/questions/51167768/sobel-edge-detection-using-opencv
    grad_x = cv2.Sobel(img2, cv2.CV_8U, 1, 0, ksize=5)
    grad_y = cv2.Sobel(img2, cv2.CV_8U, 0, 1, ksize=5)
    #grad2 = cv2.Sobel(img2, cv2.CV_8U, 1, 1, ksize=5)

    #grad = np.sqrt(grad_x ** 2 + grad_y ** 2)

    img_sobel_gesamt = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0.0)
    # grad_norm = (grad * 255 / grad.max()).astype(np.uint8)
    #
    #grad3 = (grad_x + grad_y)

    # abs_grad_x = cv2.convertScaleAbs(grad_x)
    # abs_grad_y = cv2.convertScaleAbs(grad_y)
    #
    # grad4 = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    # grad4 = cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)

    #if numpy.array_equiv(grad_norm, grad2): print("suc")


print()
print("Best Times:")

# timer(cv2.GaussianBlur, 0, 0, img, (3, 3), 0)
# print(f'Gaussian Blur 3x3:   {results[0]} ns')
#
# timer(cv2.GaussianBlur, 1, 0, img, (5, 5), 0)
# print(f"Gaussian Blur 5x5:   {results[1]} ns")
#
# timer(cv2.GaussianBlur, 2, 0, img, (55, 55), 0)
# print(f"Gaussian Blur 55x55: {results[2]} ns")
#
# timer(cv2.medianBlur, 3, 0, img, 5)  # (5,5) ?
# print(f"Median Blur 5x5:     {results[3]} ns")

# timer(cv2.blur, 4, 0, img, ksize=(5, 5))
# print(f"Normalized Blur 5x5:    {results[4][0]} ns")

# timer(cv2.bilateralFilter, 5, 1, img, 5, 5 * 2, 5 / 2)  # slow?
# print(f"Bilateral Blur 5x5:     {results[5][0]} ns")

# # # # # # blurs sw

# timer(cv2.GaussianBlur, 0, 1, img2, ksize=(3, 3), sigmaX=0)
# print(f'Gaussian Blur sw 3x3:   {results[0][1]} ns')
#
# timer(cv2.GaussianBlur, 1, 1, img2, ksize=(5, 5), sigmaX=0)
# print(f"Gaussian Blur sw 5x5:   {results[1][1]} ns")
#
# timer(cv2.GaussianBlur, 2, 1, img2, ksize=(55 ,55), sigmaX=0)
# print(f"Gaussian Blur sw  55x55:{results[2][1]} ns")
#
# timer(cv2.medianBlur, 3, 1, img2, ksize=5)
# print(f"Median Blur sw 5x5:     {results[3][1]} ns")
#
# timer(cv2.blur, 4, 1, img2, ksize=(5 ,5))
# print(f"Normalized Blur sw 5x5: {results[4][1]} ns")
#
# timer(cv2.bilateralFilter, 5, 1, img2, 5, 5 * 2, 5 / 2)  # slow?
# print(f"Bilateral Blur sw 5x5:  {results[5][1]} ns")

# # # # # #

# timer(cv2.Sobel, 6, 1, img2, cv2.CV_8U, 1, 0, ksize=5)
# print(f"Sobel X 5x5:            {results[6][1]} ns")
#
# timer(cv2.Sobel, 7, 1, img2, cv2.CV_8U, 0, 1, ksize=5)
# print(f"Sobel Y 5x5:            {results[7][1]} ns")
#
timer(sobel_edge_detector, 8, 1)
print(f"Sobel Gesamt 5x5:       {results[8][1]} ns")

# timer(cv2.Laplacian, 10, 1, img2, cv2.CV_8U, ksize=5)
# print(f"Laplace:               {results[10][1]} ns")

# timer(cv2.Canny, 9, 1, img2, 255 / 3, 255)
# print(f"Canny:               {results[9][1]} ns")


# system_info
