from flask import Flask, request, jsonify, send_file, make_response
import os
import io
import json
from werkzeug.datastructures import FileStorage
import base64
# from algo import algo

app = Flask(__name__)

# Dossier contenant les images par sélections
IMAGE_FOLDER = "../images_selection"
GB_FOLDER = "../images_gb"
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['GB_FOLDER'] = GB_FOLDER


count = 0


# Route : getInterface (GET pour envoyer les images contenues dans les dossiers de sélection)
@app.route('/getInterface', methods=['GET'])
def get_interface():
    boundary = "----WebKitFormBoundary"  # Définir une limite pour séparer les parties form-data
    buffer = io.BytesIO()

    # Construire le JSON des métadonnées
    interface_data = []
    for selection in os.listdir(app.config['IMAGE_FOLDER']):
        selection_path = os.path.join(app.config['IMAGE_FOLDER'], selection)
        if os.path.isdir(selection_path):
            images = [image for image in os.listdir(selection_path) if os.path.isfile(os.path.join(selection_path, image))]
            interface_data.append({"selection": selection, "images": images})

    # Ajouter le JSON comme une partie form-data
    json_data = json.dumps(interface_data)
    buffer.write(f"--{boundary}\r\n".encode())
    buffer.write(f"Content-Disposition: form-data; name=\"metadata\"\r\n".encode())
    buffer.write("Content-Type: application/json\r\n\r\n".encode())
    buffer.write(json_data.encode())
    buffer.write("\r\n".encode())

    # Ajouter les images comme parties form-data
    for selection in os.listdir(app.config['IMAGE_FOLDER']):
        selection_path = os.path.join(app.config['IMAGE_FOLDER'], selection)
        if os.path.isdir(selection_path):
            for image in os.listdir(selection_path):
                image_path = os.path.join(selection_path, image)
                if os.path.isfile(image_path):
                    with open(image_path, "rb") as img_file:
                        buffer.write(f"--{boundary}\r\n".encode())
                        buffer.write(f"Content-Disposition: form-data; name=\"images\"; filename=\"{image}\"\r\n".encode())
                        buffer.write("Content-Type: image/png\r\n\r\n".encode())
                        buffer.write(img_file.read())
                        buffer.write("\r\n".encode())

    # Terminer la réponse form-data
    buffer.write(f"--{boundary}--\r\n".encode())
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    return response


# Route : sendResult (POST pour envoyer les choix de l'utilisateur à l'algorithme)
@app.route('/sendResult', methods=['POST'])
def send_result():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid format, expected a list of dictionaries"}), 400

        # Construire le chemin vers l'image générée
        image_path = os.path.join(app.config['GB_FOLDER'], temp(data))

        if not os.path.exists(image_path):
            return jsonify({"error": "Image not found"}), 404

        # Retourner l'image directement
        return send_file(image_path, mimetype='image/webp')

    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 400

def temp(json):
    return "ecommerce_349_tabbar_withmenu@2x.webp"

if __name__ == "__main__":
    app.run(debug=True)
