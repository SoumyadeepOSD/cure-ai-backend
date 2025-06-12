import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from huggingface_hub import hf_hub_download
from app.image_analysis import analyze_cancer_image
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
import tensorflow as tf
from PIL import Image
import numpy as np
import io


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Class labels
class_names = ["Bengin cases", "Malignant cases", "Normal cases"]

try:
    model_path = hf_hub_download(
        repo_id="SoumyadeepOSD123/vgg16-lung-cancer-model",
        filename="VGG16.h5"
    )

    model = tf.keras.models.load_model(model_path, compile=False)
except Exception as e:
    raise RuntimeError(f"🔥 Failed to load model: {e}")


@app.get("/")
def read_root():
    return {"msg": "Lung Cancer Prediction API is running."}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image format.")

    if model is None:
        raise HTTPException(status_code=500, detail="Model not available")

    contents = await file.read()
    try:
        image = Image.open(io.BytesIO(contents)).resize(
            (224, 224)).convert("RGB")
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)
        label = class_names[np.argmax(preds)]
        confidence = float(np.max(preds))

        return {"prediction": label, "confidence": confidence}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_cancer_image(contents)
    return JSONResponse(content=result)
