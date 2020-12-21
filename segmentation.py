import numpy as np
import cv2

# Calcul de la teinte
def computeHue(r, g, b, delta, colorMax):
    if delta == 0.00:
        return 0.

    if colorMax == r:
        return 60 * (((g - b) / delta) % 6)

    if colorMax == g:
        return 60 * (((b - r) / delta) + 2)

    if colorMax == b:
        return 60 * (((r - g) / delta) + 4)


# Calcul de la saturation
def computeSaturation(delta, colorMax):
    return 0 if colorMax == 0 else delta / colorMax

# Conversion de l'espace RGB en HSV
def RGB2HSV_Pixel(rgbPixel):
    b, g, r = rgbPixel / 255
    colorMax = max(r, g, b)
    delta = colorMax - min(r, g, b)
    return computeHue(r, g, b, delta, colorMax), computeSaturation(delta, colorMax), colorMax


# Algorithme d'extraction du fond vers sur les gros plans
def normalViewGreenFilter(in_img):
    height, width, _ = in_img.shape
    tmp_img = np.zeros((height, width, 3), dtype=np.ubyte)
    kernel11 = np.ones((11, 11), np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            h, s, _ = RGB2HSV_Pixel(in_img[y, x])
            # Valeurs de seuillage saturation = 0.3 ou teinte [95;140]
            if s < 0.3 or h <= 95. or h >= 140.:
                tmp_img[y, x] = (255, 255, 255)

    # On utilise des filtres morphologique pour améliorer le rendu avec un kernel carré 11*11
    """
    On effectue une fermeture pour combler les trous dans la structure du mannequin,
    puis une ouverture pour lisser les bords du mannequin
    et supprimer les petites particules blanc isolé dans le fond vert
    """
    close_img = cv2.morphologyEx(tmp_img, cv2.MORPH_CLOSE, kernel11)
    return cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel11)


# Algorithme d'extraction du fond vers sur les gros plans
def largeViewGreenFilter(in_img):
    height, width, _ = in_img.shape
    tmp_img = np.zeros((height, width, 3), dtype=np.ubyte)
    kernel11 = np.ones((11, 11), np.uint8)
    kernel27 = np.ones((27, 27), np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            h, s, _ = RGB2HSV_Pixel(in_img[y, x])
            # Large view green screen filter
            if s < 0.45 and (h <= 95. or h >= 140.):
                tmp_img[y, x] = (255, 255, 255)


    # On utilise des filtres morphologique pour améliorer le rendu avec un kernel carré 11*11
    """
    On effectue une fermeture pour combler les trous dans la structure du mannequin,
    puis une ouverture pour lisser les bords du mannequin
    et supprimer les petites particules blanc isolé dans le fond vert
    """
    close_img = cv2.morphologyEx(tmp_img, cv2.MORPH_CLOSE, kernel11)
    open_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel11)

    # Cette forte ouverture a permis de supprimer les cameras présente dans le fond vert tout en préservant le mannequin
    return cv2.morphologyEx(open_img, cv2.MORPH_OPEN, kernel27)


def computeGreenExtractionMask(filterFunc, in_img):
    return filterFunc(in_img)


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
