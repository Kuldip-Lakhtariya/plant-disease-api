# 🌿 Plant Disease Detection API

A production-ready deep learning REST API that detects **15 plant diseases** from leaf images using **EfficientNetB0** transfer learning — deployed live on Render.

🔗 **Live Demo:** [https://plant-disease-api-l7mi.onrender.com](https://plant-disease-api-l7mi.onrender.com)

---

##  Model Performance

| Metric | Value |
|--------|-------|
| Validation Accuracy | **93.09%** |
| Classes | 15 |
| Base Model | EfficientNetB0 (ImageNet) |
| Trainable Parameters | 19,215 / 4,000,000 |
| Confidence Threshold | 0.60 (production safety) |
| Worst Class | Tomato Early Blight (60% — visual similarity) |

---

##  Supported Classes

| Crop | Disease |
|------|---------|
| Pepper Bell | Bacterial Spot, Healthy |
| Potato | Early Blight, Late Blight, Healthy |
| Tomato | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy |

---

##  Architecture & Tech Stack

```
Input Image (224x224)
       ↓
EfficientNetB0 (frozen, ImageNet weights)
       ↓
GlobalAveragePooling2D
       ↓
Dense(128, ReLU)
       ↓
Dropout(0.3)
       ↓
Dense(15, Softmax)
       ↓
Confidence Threshold Filter (< 0.60 → warning)
       ↓
JSON Response
```

**Stack:** TensorFlow · Keras · Flask · Gunicorn · Docker · Render

---

##  API Endpoints

### `GET /`
Returns the HTML frontend for image upload.

### `POST /predict`
Accepts a leaf image and returns disease prediction.

**Request:**
```bash
curl -X POST https://plant-disease-api-l7mi.onrender.com/predict \
  -F "image=@leaf.jpg"
```

**Response (high confidence):**
```json
{
  "predicted_class": "Tomato_Late_blight",
  "confidence": 0.9342,
  "warning": null
}
```

**Response (low confidence):**
```json
{
  "predicted_class": null,
  "confidence": 0.4821,
  "warning": "Low confidence — retake image in better lighting"
}
```

### `GET /health`
Health check endpoint.
```json
{"status": "running"}
```

---

##  Docker

This app is containerized using Docker for consistent deployment across environments.

```bash
# Build image
docker build -t plant-disease-api .

# Run container
docker run -p 10000:10000 plant-disease-api
```

The Dockerfile:
- Uses `python:3.11-slim` base image
- Installs Rust (required for some TensorFlow dependencies)
- Filters out Windows-only packages before install
- Exposes port 10000 (Render's free tier requirement)
- Starts with Gunicorn for production-grade serving

---

##  Project Structure

```
plant-disease-api/
├── app.py                  # Flask REST API
├── best_model.keras        # Trained EfficientNetB0 model
├── Dockerfile              # Container configuration
├── Procfile                # Render start command
├── requirements.txt        # Python dependencies
└── templates/
    └── index.html          # Frontend UI
```

---

##  Key Production Decisions

- **Confidence Thresholding** — Predictions below 60% return a warning instead of a wrong answer. Better to say "uncertain" than to mislead a farmer.
- **Transfer Learning** — Only 19K parameters trained out of 4M total. EfficientNetB0 frozen as feature extractor.
- **Relative Model Path** — `load_model('best_model.keras')` instead of hardcoded Windows path. Works on any OS.
- **Gunicorn over Flask dev server** — Handles concurrent requests in production.
- **Docker layer caching** — `requirements.txt` copied before source code so pip install is cached across rebuilds.

---

##  Explainability

Grad-CAM implemented in training notebook to visualize which leaf regions activate the model's predictions.

---

##  Training Details

- **Dataset:** PlantVillage (15 classes)
- **Strategy:** Two-phase training (Phase 2 skipped — model plateaued at 93%)
- **Phase 1:** Train only top layers (EfficientNetB0 frozen)
- **Input Size:** 224×224×3

---

## 👤 Author

**Kuldip Lakhtariya** — B.Tech Student | ML & DL Engineer

🔗 [GitHub](https://github.com/Kuldip-Lakhtariya) · [Live App](https://plant-disease-api-l7mi.onrender.com)
