import json
import numpy as np
from collections import Counter
from PIL import ImageColor

PONDERATION = {
    "typeSite":1, #str
    "typeMenu":0.3, #str
    "couleurDominante":0.3, #Hex
    "paletteCouleurs":0.2, #Hex
    "contraste":0.3, #float
    "scroll":0.1, #str
    "nbElement":0.05, #int
    "elementSize":0.15, #float
    "searchBar":0.8, #bool
    "layout":0.5, #str
    "typographie":0.15, #str
    "taillePolice":0.2, #str
    "boutonsActions":0.8, #int
    "barreNavigation":0.75, #str
    "densiteVisuelle":0.6, #str
    "contenuPrincipal":0.9, #str
    "theme":0.9, #str
    "presenceImages":0.8, #bool
    "presenceGraphiques":0.7 #bool
}

#Extraction json
def extractData(jsonFile)->list:
    with open(jsonFile) as f:
        d = json.load(f)
    return d

#fonction pour retourner les critères selon les choix
def returnDataChoice(choice:dict,pictureList:dict)->list:
    listChoix = np.array([])
    for value in choice:
        listChoix = np.append(pictureList[value])
    return listChoix

#retourne la valeur choisie d'un dictionnaire
def getValues(firstKey:dict,secondKey:str):
    return firstKey[secondKey]

#retourne la valeure qui a une récurrence maximale selon la clé
def returnMaxValues(listChoice,key:str):
    liste = []
    for e in listChoice:
        liste.append(getValues(e,key))
    return max(Counter(liste),key=Counter(liste).get)

#retourne le score de comparaison entre deux valeurs de même clé de deux dictionnaires
def comparaison(dictChoice:dict, dictBase:dict,value:str)->int:
    if dictChoice[value]==dictBase[value]:
        return 1
    else:
        return 0 

#conversion Hexadécimal
def conversionHex(hexColor:str)->list:
    return ImageColor.getrgb(hexColor)

#comparaisonHexadecimal
def comparaisonHex(dictChoice:dict,dictBase:dict,value:str)->float:
    value = 0
    rgbChoice = conversionHex(dictChoice[value])
    rgbBase = conversionHex(dictBase[value])
    for i in range(len(rgbChoice)):
        value += min(rgbChoice[i],rgbBase[i])/max(rgbChoice[i],rgbBase[i])
    return value/len(rgbChoice)

#comparaisonfloat
def comparaisonFloat(dictChoice:dict,dictBase:dict,value:str)->float:
    return min(dictChoice[value],dictBase[value])/max(dictChoice[value],dictBase[value])


def main(jsonChoices):
    #dictionnare du json des images
    pictureDict = extractData('test.json')
    #copie de la liste précédente qui sera manipulée
    pictureTri = pictureDict.deepcopy()
    #on retourne une liste des choix et leurs valeurs
    listChoice = returnDataChoice(extractData(jsonChoices),pictureDict)
    #
    