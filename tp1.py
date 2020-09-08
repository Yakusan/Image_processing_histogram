import numpy as np
import cv2
import sys

nbArg = len(sys.argv)

if nbArg != 3:
    print('programme <nom fichier d\'entrée (.png)> <nom fichier de sortie (.png)>')
    exit()

img_in = cv2.imread(sys.argv[1]).astype(np.ubyte)

h, w, _ = img_in.shape

img_out = np.zeros((h, w, 3), dtype=np.ubyte)

# Algo extraction fond vert
for y in range(0, h):
    for x in range(0, w):
        if img_in[y, x, 1]  == 0:
            img_out[y,x] = (255, 255, 255)

cv2.imwrite(sys.argv[2], img_out)
