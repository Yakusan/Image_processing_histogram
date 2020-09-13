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
            'Programme <Chemin de l\'image d\'entrée (.png)> <Chemin du repertoire de l\'image de sortie (.png)> '
            'Optionnel: <fonction de filtrage>')
        print(
            'Fonction de filtrage:\n\t0 : Filtre teinte verte\n\t1 : Filtre de saturation passe bas\n\n\tPar defaut: '
            'Filtre teinte verte')
        exit()

    filterFunc = mywork.greenFilter
    if nbArg == 4:
        numFilter = int(sys.argv[3])
        if numFilter == 0:
            filterFunc = mywork.greenFilter
        elif numFilter == 1:
            filterFunc = mywork.lowPassSaturationFilter
        else:
            filterFunc = mywork.greenFilter

    out_img = mywork.computeGreenExtractionMask(cv2.imread(sys.argv[1]).astype(np.float64), filterFunc)
    in_filename = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
    cv2.imwrite(sys.argv[2] + '/' + in_filename + '_mask.png', out_img)
