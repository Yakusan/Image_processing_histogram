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
    directory = sys.argv[2]
    if nbArg == 4:
        isLargePlan = bool(sys.argv[3])
        if isLargePlan:
            filterFunc = mywork.largeViewGreenFilter
            files = glob.glob(sys.argv[1] + '/Plan large/*.png')
            directory = directory + '/Plan large'

    for file in files:
        out_img = mywork.computeGreenExtractionMask(filterFunc, cv2.imread(file).astype(np.float64))
        in_filename = os.path.split(os.path.splitext(file)[0])[1]
        cv2.imwrite(directory + '/' + in_filename + '_mask.png', out_img)
