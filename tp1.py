import numpy as np
import cv2
import sys
import os
import glob
import mywork

if __name__ == '__main__':
    nbArg = len(sys.argv)

    if nbArg < 3 or nbArg > 4:
        print('Usage :')
        print(
            'Programme <Dossier racine des images d\'entrée (.png)> <Chemin du repertoire pour '
            'generer l\'image de sortie (.png)> Optionnel: <C\'est un plan large ?>')
        print(
            'Plan large ? True or False\n\n\tPar defaut: False')
        exit()

    filterFunc = mywork.normalViewGreenFilter
    files = glob.glob(sys.argv[1] + '/*.png')
    if nbArg == 4:
        isLargePlan = bool(sys.argv[3])
        if isLargePlan:
            filterFunc = mywork.largeViewGreenFilter
            files = glob.glob(sys.argv[1] + '/Plan large/*.png')

    # kernel5 = np.ones((5, 55), np.uint8)
    kernel11 = np.ones((11, 11), np.uint8)

    for file in files:
        result_img = mywork.computeGreenExtractionMask(cv2.imread(file).astype(np.float64), filterFunc)

        close_img = cv2.morphologyEx(result_img, cv2.MORPH_CLOSE, kernel11)
        out_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel11)

        in_filename = os.path.split(os.path.splitext(file)[0])[1]
        cv2.imwrite(sys.argv[2] + '/' + in_filename + '_mask.png', out_img)
