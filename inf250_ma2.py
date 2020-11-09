# -*- coding: utf-8 -*-

"""
INF250 Mandatory assignment 2
Sharpen and edge detection
"""

__author__ = "Kristian Gunder Kramås"
__email__ = "kristiankramas@outlook.com"


img_path = "./AthenIR.png"


def detectEdges(img=img, edge_operator="prewitt"):
    output = img

    return {
        "prewitt": output,
        "sobel": output,
        "canny": output,
    }[edge_operator]


def sharpen(img=img, method="la_place"):
    output = img

    return {
        "la_place": output,
        "usm": output,
    }[method]