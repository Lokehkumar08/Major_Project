import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load model
MODEL_PATH = "cancer_diagnosis_model.keras"

# Clear any existing TensorFlow session before loading model
tf.keras.backend.clear_session()
model = tf.keras.models.load_model(MODEL_PATH)

# Define class labels based on your dataset folder structure
class_labels = [
    "Actinic keratosis", "Atopic Dermatitis", "Benign keratosis", 
    "Dermatofibroma", "Melanocytic nevus", "Melanoma", 
    "Squamous cell carcinoma", "Tinea Ringworm Candidiasis", "Vascular lesion"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    
    # Secure the filename and save it
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    print(f"Processing File: {filepath}")  # Debugging: Ensure file is saved

    # Preprocess the image
    img = load_img(filepath, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Important preprocessing step

    print(f"Image Shape Before Prediction: {img_array.shape}")  # Debugging

    # Make prediction
    predictions = model.predict(img_array)
    
    print(f"Raw Predictions: {predictions}")  # Debugging: Print raw model output

    class_index = np.argmax(predictions)
    predicted_class = class_labels[class_index]  # Get class name from label list
    confidence = float(predictions[0][class_index])  # Extract confidence score

    print(f"Predicted Class: {predicted_class} with Confidence: {confidence * 100:.2f}%")  

    return render_template(
        "result.html",
        image_path=url_for("static", filename=f"uploads/{filename}"),
        predicted_class=predicted_class,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(debug=True)
