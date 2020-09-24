import numpy as np
import cv2
import sys
import os
import mywork


if __name__ == '__main__':
    nbArg = len(sys.argv)

    if nbArg < 3 or nbArg > 4:
        print('Usage :')
        print(
            'Programme <Chemin de l\'image d\'entrée (.png)> <Chemin du repertoire pour '
            'generer l\'image de sortie (.png)> Optionnel: <valeur H, S ou V niveau de gris>')
        print('\t0 : h\n\t1 : s\n\t2 : v\n\n\tPar defaut: h')
        exit()

    hsvOption = int(sys.argv[3]) if nbArg == 4 else 0

    strMode = ''
    if hsvOption == 0:
        strMode = 'hue'
    elif hsvOption == 1:
        strMode = 'saturation'
    elif hsvOption == 2:
        strMode = 'value'

    out_img = mywork.computeGrayImg(cv2.imread(sys.argv[1]).astype(np.float64), hsvOption)
    in_filename = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
    cv2.imwrite(sys.argv[2] + '/' + in_filename + '_gray_' + strMode + '.png', out_img)
