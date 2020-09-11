import numpy as np
import cv2
import sys

def computeHue(r, g , b, delta, colorMax):
    if(delta == 0):
        return 0

    if(colorMax == r):
        return 60 * (((g - b) / delta) % 6)

    elif(colorMax == g):
        return 60 * (((b - r) / delta) + 2)

    elif(colorMax == b):
        return 60 * (((r - g) / delta) + 4)

def computeSaturation(delta, colorMax):
    return 0 if (colorMax == 0) else delta / colorMax

nbArg = len(sys.argv)

if nbArg != 3:
    print('programme <nom fichier d\'entrée (.png)> <nom fichier de sortie (.png)>')
    exit()

img_in = cv2.imread(sys.argv[1]).astype(np.float64)

h, w, _ = img_in.shape

img_out = np.zeros((h, w, 3), dtype=np.ubyte)

# Algo extraction fond vert
for y in range(0, h):
    for x in range(0, w):
        b, g, r  = img_in[y, x]
        colorMax = max(r, g, b)
        colorMin = min(r, g, b)
        delta    = colorMax - colorMin

        (h, s, v) = (computeHue(r, g, b, delta, colorMax), computeSaturation(delta, colorMax), colorMax)

        # green hsv parameter threshold
        if not ((h >= 65 and h <= 180) and s > 0.15 and v > 0.1):
            img_out[y,x] = (255, 255, 255)

cv2.imwrite(sys.argv[2], img_out)
