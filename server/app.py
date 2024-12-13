from flask import Flask, request, jsonify, send_file, make_response
import os
from flask_cors import CORS
import algorithm as algo

# Activer CORS sur l'application Flask

app = Flask(__name__)
CORS(app)
# Dossier contenant les images par sélections
IMAGE_FOLDER = "../images_selection"
GB_FOLDER = "../images_gb"
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['GB_FOLDER'] = GB_FOLDER

# Variable globale pour gérer l'index des dernières listes envoyées
last_index = 0

# Route : getInterface (GET pour envoyer les images avec sélection formatée)
@app.route('/getInterface', methods=['GET'])
def get_interface():
    global last_index

    # Récupérer toutes les sélections disponibles
    all_selections = [
        selection for selection in os.listdir(app.config['IMAGE_FOLDER'])
        if os.path.isdir(os.path.join(app.config['IMAGE_FOLDER'], selection))
    ]

    # Limiter à 3 sélections, en utilisant un modulo pour boucler
    num_selections = len(all_selections)
    if num_selections == 0:
        return jsonify({"error": "No selections available"}), 400

    selected_selections = [
        all_selections[(last_index + i) % num_selections] for i in range(3)
    ]
    last_index = (last_index + 3) % num_selections

    # Construire le JSON des métadonnées
    interface_data = []
    for index, selection in enumerate(selected_selections, start=1):
        selection_path = os.path.join(app.config['IMAGE_FOLDER'], selection)
        images = [
            {"image": image} for image in os.listdir(selection_path)
            if os.path.isfile(os.path.join(selection_path, image))
        ]

        interface_data.append({"selection": index, "images": images})

    return jsonify(interface_data)

# Route : sendResult (POST pour envoyer les choix de l'utilisateur à l'algorithme)
@app.route('/sendResult', methods=['POST'])
def send_result():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid format, expected a list of dictionaries"}), 400

        # Appelle algo.main avec les données
        result_image = algo.main(data)
        return jsonify({"image": result_image})

    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
