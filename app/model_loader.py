import os
import tensorflow as tf

# Path to the local model file (adjusted for your current placement)
MODEL_LOCAL_PATH = "app/MobileNetV2_LungCancer.h5"

def load_model_once():
    if not os.path.exists(MODEL_LOCAL_PATH):
        raise FileNotFoundError(f"❌ Model not found at {MODEL_LOCAL_PATH}")

    print(f"✅ Loading model from: {MODEL_LOCAL_PATH}")
    return tf.keras.models.load_model(MODEL_LOCAL_PATH, compile=False)
