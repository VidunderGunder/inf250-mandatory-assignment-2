# -*- coding: utf-8 -*-

"""
INF250 Mandatory assignment 2

Sharpening and edge detection

See: https://github.com/VidunderGunder/inf250-mandatory-assignment-2
"""

__author__ = "Kristian Gunder Kramås"
__email__ = "kristiankramas@outlook.com"

from cv2 import cv2
import numpy as np
import os


def detect_edges(img, edge_operator="prewitt"):
    """
    Returns the result from one of the edge operators,
    prewitt, sobel or canny

    Based on:
        https://gist.github.com/rahit/c078cabc0a48f2570028bff397a9e154
        https://docs.opencv.org/master/da/d22/tutorial_py_canny.html

    Parameters:
    -----------
    img : np.ndarray
        Image to detect blobs in
    operator : string
        "prewitt", "canny" or "laplace"
        Defaults to "prewitt"

    Returns:
    --------
    output : np.ndarray(np.uint)
        Resulting image from the edge operator
        or given image if invalid edge operator
    """

    # Blurred version of the image, to reduce noise and facilitate
    # spotting actual edges as generally recommended by OpenCV, e.g.:
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
    img_gaussian = cv2.GaussianBlur(img, (3, 3), 0)

    # Functions to use in switch
    def prewitt():
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        return cv2.filter2D(img_gaussian, -1, kernelx) + cv2.filter2D(
            img_gaussian, -1, kernely
        )

    def sobel():
        img_sobelx = cv2.Sobel(img_gaussian, cv2.CV_8U, 1, 0, ksize=3)
        img_sobely = cv2.Sobel(img_gaussian, cv2.CV_8U, 0, 1, ksize=3)
        return img_sobelx + img_sobely

    def canny():
        return cv2.Canny(img, threshold1=50, threshold2=90)

    # Switch
    # Returns original image if no valid edge operator
    return {
        "prewitt": prewitt(),
        "sobel": sobel(),
        "canny": canny(),
    }.get(edge_operator.lower(), img)


def sharpen(img, method="la_place"):
    """
    Performs an image sharpening using laplace filter or unsharpen mask (USM)

    Based on:
        https://docs.opencv.org/3.4/d5/db5/tutorial_laplace_operator.html
        https://stackoverflow.com/questions/4993082/how-can-i-sharpen-an-image-in-opencv (top answer as of 10.11.2020)

    Parameters:
    -----------
    img : np.ndarray
        Image to sharpen.
    operator : string
        "la_place" or "usm"
        Defaults to "la_place"

    Returns:
    --------
    output : np.ndarray(np.uint)
        Resulting image from the given method
        or given image if invalid method
    """

    # Functions to use in switch
    def la_place():
        dst = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
        return cv2.convertScaleAbs(dst)

    def usm():
        img2 = cv2.GaussianBlur(img, (0, 0), 2.0)
        return cv2.addWeighted(img, 1, img2, -0.5, 0, img)

    # Switch
    # Returns original image if no valid edge operator
    return {
        "la_place": la_place(),
        "usm": usm(),
    }.get(method.lower(), img)


def export(img, name):
    """
    Exports image to output directory

    Parameters:
    -----------
    img : np.ndarray
        Image to export
    name : string
        Filename
    """
    output_dir = "./output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cv2.imwrite(f"{output_dir}/{name}.png", img)


def show(img, name):
    """
    Shows image

    Parameters:
    -----------
    img : np.ndarray
        Image to show
    name : string
        Header
    """
    cv2.imshow(name, img)
    input("Press enter to continue")


if __name__ == "__main__":
    img_path = "./AthenIR.png"
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    edge_operators = [
        "prewitt",
        "sobel",
        "canny",
    ]

    methods = [
        "la_place",
        "usm",
    ]

    for operator in edge_operators:
        result = detect_edges(img, operator)
        export(result, operator)

    for method in methods:
        result = sharpen(img, method)
        export(result, method)