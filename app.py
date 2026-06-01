import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from io import BytesIO

app = Flask(__name__)

model = tf.keras.models.load_model('best_model.keras')

class_names = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___healthy',
    'Potato___Late_blight',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

CONFIDENCE_THRESHOLD = 0.60

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image sent'}), 400

    file = request.files['image']

    img = tf.keras.utils.load_img(BytesIO(file.read()), target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    preds = model.predict(img_array, verbose=0)
    confidence = float(np.max(preds))
    class_index = int(np.argmax(preds))
    class_name = class_names[class_index]

    if confidence < CONFIDENCE_THRESHOLD:
        return jsonify({
            'predicted_class': None,
            'confidence': round(confidence, 4),
            'warning': 'Low confidence — retake image in better lighting'
        })

    return jsonify({
        'predicted_class': class_name,
        'confidence': round(confidence, 4),
        'warning': None
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    app.run(debug=True)