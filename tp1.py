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
            'generer l\'image de sortie (.png)> Optionnel: <C\'est un plan large ?>')
        print(
            'Plan large ? True or False\n\n\tPar defaut: False')
        exit()

    filterFunc = mywork.normalViewGreenFilter
    if nbArg == 4:
        isLargePlan = bool(sys.argv[3])
        if isLargePlan:
            filterFunc = mywork.largeViewGreenFilter

    out_img = mywork.computeGreenExtractionMask(cv2.imread(sys.argv[1]).astype(np.float64), filterFunc)
    in_filename = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
    cv2.imwrite(sys.argv[2] + '/' + in_filename + '_mask.png', out_img)
