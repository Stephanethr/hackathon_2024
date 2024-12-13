import json
import numpy as np
from collections import Counter
from PIL import ImageColor

PONDERATION = {
    "typeSite":10, #str
    "typeMENU":0.3, #str
    "couleurDominante":6, #Hex
    "paletteCouleurs":4, #Hex
    "contraste":2, #float
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
    res = 0
    rgbChoice = conversionHex(dictChoice[value])
    rgbBase = conversionHex(dictBase[value])
    for i in range(len(rgbChoice)):
        res += min(rgbChoice[i],rgbBase[i])/max(rgbChoice[i],rgbBase[i])
    return res/len(rgbChoice)

def comparaisonHexList(listChoice:list,listBase:list)->float:
    res = 0
    for i in range(len(listChoice)):
        rgbChoice = conversionHex(listChoice[i])
        rgbBase = conversionHex(listBase[i])
        for j in range(len(listChoice)):
            res += min(rgbChoice[j],rgbBase[j])/max(rgbChoice[j],rgbBase[j])
        return res/9
    
#comparaisonfloat
def comparaisonFloat(dictChoice:dict,dictBase:dict,value:str)->float:
    return min(dictChoice[value],dictBase[value])/max(dictChoice[value],dictBase[value])

#return score
def score(dictChoice:dict,dictBase:dict)->float:
    global PONDERATION
    value = 0
    for e in dictBase:
        if isinstance(e,str) or isinstance(e,bool):
            res = comparaison(dictBase,dictChoice,e)
        elif isinstance(e,float):
            res = comparaisonFloat(dictChoice,dictBase,e)
        elif isinstance(e,list):
            res = comparaisonHexList(dictChoice[e], dictBase[e])
        else:
            res = comparaisonHex(dictChoice,dictBase,e)
        value += res * PONDERATION[e]
    return value
    