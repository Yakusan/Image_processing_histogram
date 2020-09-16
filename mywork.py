import numpy as np


def computeHue(r, g, b, delta, colorMax):
    if delta == 0.00:
        return 0.

    if colorMax == r:
        return 60 * (((g - b) / delta) % 6)

    if colorMax == g:
        return 60 * (((b - r) / delta) + 2)

    if colorMax == b:
        return 60 * (((r - g) / delta) + 4)


def computeSaturation(delta, colorMax):
    return 0 if colorMax == 0 else delta / colorMax


def RGB2HSV_Pixel(rgbPixel):
    b, g, r = rgbPixel / 255
    colorMax = max(r, g, b)
    delta = colorMax - min(r, g, b)
    return computeHue(r, g, b, delta, colorMax), computeSaturation(delta, colorMax), colorMax


def normalViewGreenFilter(h, s, out_img_nvgf, x, y):
    # Normal green screen filter
    if s < 0.3 or h <= 95. or h >= 140.:
        out_img_nvgf[y, x] = (255, 255, 255)


def largeViewGreenFilter(h, s, out_img_lvgf, x, y):
    # Large view green screen filter
    if s < 0.45 and (h <= 95. or h >= 125.):
        out_img_lvgf[y, x] = (255, 255, 255)


def computeGreenExtractionMask(in_img, filter):
    height, width, _ = in_img.shape
    out_img = np.zeros((height, width, 3), dtype=np.ubyte)
    for y in range(0, height):
        for x in range(0, width):
            h, s, _ = RGB2HSV_Pixel(in_img[y, x])

            filter(h, s, out_img, x, y)

    return out_img


def computeGrayImg(in_img, hsvOptions):
    height, width, _ = in_img.shape
    out_img_gray = np.zeros((height, width, 3), dtype=np.ubyte)
    for y in range(0, height):
        for x in range(0, width):
            h, s, v = RGB2HSV_Pixel(in_img[y, x])

            if hsvOptions == 0:
                value = h / 360 * 255
            elif hsvOptions == 1:
                value = s * 255
            elif hsvOptions == 2:
                value = v * 255
            else:
                value = 0

            out_img_gray[y, x] = (value, value, value)

    return out_img_gray


def computeHSVImg(in_img):
    height, width, _ = in_img.shape
    out_img_hsv = np.zeros((height, width, 3), dtype=np.float64)
    for y in range(0, height):
        for x in range(0, width):
            out_img_hsv[y, x] = RGB2HSV_Pixel(in_img[y, x])

    return out_img_hsv
