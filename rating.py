import cv2
import numpy

from numpy import ndarray


def rate_image(frame: ndarray):
    """ Rating Images based on edges found with Canny Edge-Detector"""
    edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.Canny(edges, 0, 30, edges, 3)
    cv2.Canny(edges, 50, 150, edges, 3)  # seems to be better suited
    return len(numpy.argwhere(edges != 0))


