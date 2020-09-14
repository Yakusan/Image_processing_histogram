import numpy as np
import cv2
import sys
import os
import mywork


def computeGrayImg(in_img, hsvOptions):
    height, width, _ = in_img.shape
    out_img_gray = np.zeros((height, width, 3), dtype=np.ubyte)
    for y in range(0, height):
        for x in range(0, width):
            h, s, v = mywork.RGB2HSV_Pixel(in_img[y, x])

            if hsvOptions == 0:
                value = h
            elif hsvOptions == 1:
                value = s * 100
            elif hsvOptions == 2:
                value = v * 100
            else:
                value = 0

            out_img_gray[y, x] = (value, value, value)

    return out_img_gray


if __name__ == '__main__':
    nbArg = len(sys.argv)

    if nbArg < 3 or nbArg > 4:
        print('Usage :')
        print(
            'Programme <Chemin de l\'image d\'entrée (.png)> <Chemin du repertoire de l\'image de sortie (.png)> '
            'Optionnel: <valeur H, S ou V niveau de gris>')
        print('\t0 : h\n\t1 : s\n\t2 : v\n\n\tPar defaut: h')
        exit()

    hsvOption = int(sys.argv[3]) if nbArg == 4 else 0

    out_img = computeGrayImg(cv2.imread(sys.argv[1]).astype(np.float64), hsvOption)
    in_filename = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
    cv2.imwrite(sys.argv[2] + '/' + in_filename + '_gray.png', out_img)
