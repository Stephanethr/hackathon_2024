from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Dossier contenant les images par sélections
IMAGE_FOLDER = "images"
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Route : getInterface (GET pour envoyer les images contenues dans les dossiers de sélection)
@app.route('/getInterface', methods=['GET'])
def get_interface():
    interface_data = []

    # Parcourir les sous-dossiers dans le dossier IMAGE_FOLDER
    for selection in os.listdir(app.config['IMAGE_FOLDER']):
        selection_path = os.path.join(app.config['IMAGE_FOLDER'], selection)
        if os.path.isdir(selection_path):
            images = [
                {"image": image} for image in os.listdir(selection_path)
                if os.path.isfile(os.path.join(selection_path, image))
            ]
            interface_data.append({"selection": selection, "images": images})

    return jsonify(interface_data)

# Route : sendResult (POST pour envoyer les choix de l'utilisateur à l'algorithme)
@app.route('/sendResult', methods=['POST'])
def send_result():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid format, expected a list of dictionaries"}), 400

        # Ici, le JSON reçu est transmis directement à l'algorithme
        # Exemple : appel à une fonction d'algorithme externe
        # result = your_algorithm(data)

        return jsonify({"message": "Data sent to the algorithm successfully"})
    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
