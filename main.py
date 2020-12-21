import numpy as np
import cv2
import sys
import os
import glob
import segmentation


"""
    L'objectif de ce TP est de prendre en entrée un ensemble d'image
    et de générer un masque de segmentation en sortie 
    qui classifie en deux classes, un mannequin (label blanc) et un fond vert (label noir).
    Les résultats sont disponibles dans le dossier "results".
    
    Il y a des données supplémentaires dans le dossier "extras",
    notamment des histogrammes d'image converties en HSV, qui ont permis de créer     
    cet algorithme basé sur l'analyse spectrale des images.
"""

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

    # On défini un des deux algorithme adapté pour les gros plans ou les plan larges
    filterFunc = segmentation.normalViewGreenFilter
    files = glob.glob(sys.argv[1] + '/*.png')
    directory = sys.argv[2]
    if nbArg == 4:
        isLargePlan = bool(sys.argv[3])
        if isLargePlan:
            filterFunc = segmentation.largeViewGreenFilter
            files = glob.glob(sys.argv[1] + '/Plan large/*.png')
            directory = directory + '/Plan large'

    # Pour toutes les images dans le dossier asset
    for file in files:
        # On extrait le fond vert
        out_img = segmentation.computeGreenExtractionMask(filterFunc, cv2.imread(file).astype(np.float64))
        in_filename = os.path.split(os.path.splitext(file)[0])[1]
        # On écrit le résultat de l'extraction dans un masque
        cv2.imwrite(directory + '/' + in_filename + '_mask.png', out_img)
