import os
import shutil
import tensorflow as tf
from huggingface_hub import hf_hub_download

MODEL_LOCAL_PATH = "app/models/VGG16.h5"
REPO_ID = "SoumyadeepOSD123/vgg16-lung-cancer-model"
FILENAME = "VGG16.h5"

def load_model_once():
    os.makedirs("app/models", exist_ok=True)

    if not os.path.exists(MODEL_LOCAL_PATH):
        print("📦 Model not found locally. Downloading from Hugging Face...")
        downloaded_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)

        # ✅ SAFELY move the file, even across mount points
        shutil.move(downloaded_path, MODEL_LOCAL_PATH)

        print(f"✅ Model saved at: {MODEL_LOCAL_PATH}")
    else:
        print(f"✅ Using cached model from: {MODEL_LOCAL_PATH}")

    return tf.keras.models.load_model(MODEL_LOCAL_PATH, compile=False)
