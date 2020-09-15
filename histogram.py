import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import mywork

if __name__ == '__main__':
    nbArg = len(sys.argv)

    if nbArg != 3:
        print('Usage :')
        print('Programme <Chemin de l\'image d\'entrée (.png)> <valeur HSV a mesurer>')
        print('\t0 : Teinte\n\t1 : Saturation\n\t2 : Luminosite')
        exit()

    hsvOption = int(sys.argv[2])
    if hsvOption < 0 or hsvOption > 2:
        print('Usage :')
        print('Programme <Chemin de l\'image d\'entrée (.png)> <valeur HSV a mesurer>')
        print('\t0 : Teinte\n\t1 : Saturation\n\t2 : Luminosite')
        exit()

    hsv_img = mywork.computeHSVImg(cv2.imread(sys.argv[1]).astype(np.float64))
    hist = hsv_img[:, :, hsvOption].ravel()

    hsvParam = 360 if hsvOption == 0 else 100
    if hsvOption == 0:
        strHSV = 'teinte'
    else:
        hist = hist * 100
        if hsvOption == 1:
            strHSV = 'saturation'
        else:
            strHSV = 'luminosite'

    plt.hist(hist, range=(0, hsvParam), bins=hsvParam, color='blue', edgecolor='red')
    plt.xlabel('Valeur de la ' + strHSV)
    plt.ylabel('Nombre de pixel')
    plt.title('Frequence de la ' + strHSV)
    plt.show()
