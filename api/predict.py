
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image


# # Load your pre-trained model
model = load_model('model/model2.h5')

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    image = Image.open(file).resize((48, 48)).convert('L')  # Preprocess
    img_array = np.array(image) / 255.0
    img_array = img_array.reshape(1, 48, 48, 1)

    # Perform prediction using your model (replace with actual prediction logic)
    predictions = model.predict(img_array)  # Get model predictions
    return (predictions.tolist()[0]), 200

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)