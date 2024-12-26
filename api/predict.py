from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

# Load your pre-trained model
model_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'model', 'model2.h5')
model = load_model(model_path)

app = Flask(__name__)

@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    image = Image.open(file.stream).resize((48, 48)).convert('L')  # Preprocess
    img_array = np.array(image) / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    # Perform prediction using your model
    predictions = model.predict(img_array)
    return jsonify(predictions.tolist()[0]), 200

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

