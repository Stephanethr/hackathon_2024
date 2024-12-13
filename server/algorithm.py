import json
import os
import random
import extract

# Charger le JSON des critères
def load_criteria(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Charger le JSON des sélections
def load_selections(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Trouver les critères pour une image spécifique
def get_criteria_for_image(image_name, criteria_list):
    for item in criteria_list:
        if item["image"] == image_name:
            return item["criteria"]
    return None

# Construire une liste de dictionnaires pour les images sélectionnées
def build_selected_images_criteria(criteria_file, selections_file):
    criteria_list = load_criteria(criteria_file)
    selections_list = load_selections(selections_file)

    selected_images = []

    for selection in selections_list:
        for image in selection["images"]:
            if image["is_selected"]:
                image_name = image["image"]
                criteria = get_criteria_for_image(image_name, criteria_list)
                if criteria:
                    selected_images.append({
                        "image": image_name,
                        "criteria": criteria
                    })

    return selected_images

# Construire une liste de dictionnaires pour toutes les images d'un fichier de critères
def build_all_images_criteria(criteria_file):
    criteria_list = load_criteria(criteria_file)

    all_images = []

    for item in criteria_list:
        all_images.append({
            "image": item["image"],
            "criteria": item["criteria"]
        })

    return all_images

def build_dictionaries(selections_data):
    # Chemin du fichier des critères pour les images sélectionnées (racine du projet)
    selected_criteria_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "description_images_autres.json")
    # Chemin du fichier des critères pour toutes les images (racine du projet)
    all_images_criteria_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "description_images_gb.json")

    # Générer la liste des critères des images sélectionnées
    selected_images = build_selected_images_criteria(selected_criteria_file, selections_data)

    # Générer la liste des critères pour toutes les images
    all_images = build_all_images_criteria(all_images_criteria_file)

    return selected_images, all_images

def main(json):
    selected_images, all_images = build_dictionaries(json)
    max_score = 0
    max_image_name = None

    for gb_image in all_images:
        score = 0
        for selected_image in selected_images:
            score += extract.score(selected_image['criteria'], gb_image['criteria'])
        score /= len(selected_images)

        if score > max_score:
            max_score = score
            max_image_name = gb_image["image"]

    print(max_image_name)
    print(max_score)

