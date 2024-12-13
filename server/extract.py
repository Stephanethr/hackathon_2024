from PIL import ImageColor

PONDERATION = {
    "typeSite":10, #str
    "typeMENU":0.3, #str
    "couleurDominante":8, #Hex
    "paletteCouleurs":6, #Hex
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
            res += (min(rgbChoice[j],rgbBase[j])+1)/(max(rgbChoice[j],rgbBase[j])+1)
    return res/9
 #pour la liste le return est en dehors de la boucle i, et j'ai rajouté un +1 car il y avait de la division par 0 par moment
    
#comparaisonfloat
def comparaisonFloat(dictChoice:dict,dictBase:dict,value:str)->float:
    return min(dictChoice[value],dictBase[value])/max(dictChoice[value],dictBase[value])

#return score
def score(dictChoice:dict,dictBase:dict)->float:
    global PONDERATION
    value = 0
    for e in dictBase:
        if isinstance(dictBase[e],str):
            if dictBase[e][0]=='#':
                res = comparaisonHex(dictChoice,dictBase,e)
            else:
                res = comparaison(dictBase,dictChoice,e)
        elif isinstance(dictBase[e],bool):
            res = comparaison(dictBase, dictChoice, e)
        elif isinstance(dictBase[e],float):
            res = comparaisonFloat(dictChoice,dictBase,e)
        elif isinstance(dictBase[e],list):
            res = comparaisonHexList(dictChoice[e], dictBase[e])
        value += res * PONDERATION[e]
    return value
    