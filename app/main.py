# import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image
# import numpy as np
# import io

# from app.model_loader import load_model_once   # 🔁 New loader
# from app.image_analysis import analyze_cancer_image

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Class labels
# class_names = ["Bengin cases", "Malignant cases", "Normal cases"]

# # ✅ Load model once from local cache or download
# try:
#     model = load_model_once()
# except Exception as e:
#     raise RuntimeError(f"🔥 Failed to load model: {e}")


# @app.get("/")
# def read_root():
#     return {"msg": "Lung Cancer Prediction API is running."}


# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="Invalid image format.")

#     if model is None:
#         raise HTTPException(status_code=500, detail="Model not available")

#     contents = await file.read()
#     try:
#         image = Image.open(io.BytesIO(contents)).resize((224, 224)).convert("RGB")
#         img_array = np.array(image) / 255.0
#         img_array = np.expand_dims(img_array, axis=0)

#         preds = model.predict(img_array)
#         label = class_names[np.argmax(preds)]
#         confidence = float(np.max(preds))

#         return {"prediction": label, "confidence": confidence}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# @app.post("/analyze")
# async def analyze(file: UploadFile = File(...)):
#     contents = await file.read()
#     result = analyze_cancer_image(contents)
#     return JSONResponse(content=result)
