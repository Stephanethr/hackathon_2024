import json
import numpy as np

#GLOBAL
PICTURE_LIST = np.array([])

#Extraction json reçu
def extractData(jsonFile)->list:
    with open(jsonFile) as f:
        d = json.load(f)
    return d

#fonction pour retourner
def returnDataChoice(choice:dict,pictureList:dict)->list:
    """

    Parameters
    ----------
    choice : dict
        choix de l'utilisateur.
    pictureList : dict
        base de données des images en json
    Returns
    -------
    list
        DESCRIPTION.

    """
    listChoix = np.array([])
    for value in choice:
        listChoix = np.append(pictureList[value])
    return listChoix
        
def getPresenceG(jsonFile)->bool:
    return jsonFile['presenceGraphiques']

def getPresenceI(jsonFile)->bool:
    return jsonFile['presenceImages']

def main(jsonChoice):
    pictureTri = PICTURE_LIST.copy()
    returnDataChoice