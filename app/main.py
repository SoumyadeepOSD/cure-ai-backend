import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import io
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import re

from app.model_loader import load_model_once
from app.image_analysis import analyze_cancer_image
from groq import Groq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

app = FastAPI()

# Enable CORS with specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cureai-cancer.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Class labels
class_names = ["Bengin cases", "Malignant cases", "Normal cases"]

# Initialize Groq client for text-based routes
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY environment variable is not set")

groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize Gemini for image analysis
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is not set")

gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=GOOGLE_API_KEY)

# ✅ Load model once from local cache or download
try:
    model = load_model_once()
except Exception as e:
    raise RuntimeError(f"🔥 Failed to load model: {e}")

# Pydantic models for request validation
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class RiskAnalysisRequest(BaseModel):
    age: int
    gender: str
    smoking_history: bool
    family_history: bool
    symptoms: str
    cancer_type: Optional[str] = None

class RiskAnalysisStructuredResponse(BaseModel):
    risk_factors: List[str]
    risk_score: int
    recommendations: List[str]
    risk_level: str

class ReportRequest(BaseModel):
    patient_info: Dict[str, Any]
    cancer_result: Dict[str, Any]
    risk_analysis: Optional[Dict[str, Any]] = None

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
        image = Image.open(io.BytesIO(contents)).resize((224, 224)).convert("RGB")
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)
        label = class_names[np.argmax(preds)]
        confidence = float(np.max(preds))

        return {"prediction": label, "confidence": confidence, "cancer_class": label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image format.")

    try:
        contents = await file.read()
        # Use the existing analyze_cancer_image function which uses Gemini
        result = analyze_cancer_image(contents)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/chat")
async def chat_with_ai_doctor(request: ChatMessage):
    try:
        context_str = json.dumps(request.context) if request.context else "No specific context provided"
        prompt = f"""You are an AI medical assistant specializing in lung cancer. 
        Context: {context_str}
        User Question: {request.message}
        Provide a clear, empathetic, and medically accurate response."""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/analyze-risk")
async def analyze_risk(request: RiskAnalysisRequest):
    try:
        prompt = f"""Analyze the following risk factors for lung cancer:
        Age: {request.age}
        Gender: {request.gender}
        Smoking History: {"Yes" if request.smoking_history else "No"}
        Family History: {"Yes" if request.family_history else "No"}
        Symptoms: {request.symptoms}
        Detected Cancer Type: {request.cancer_type or "Not detected"}

        Provide:
        1. Risk Level Assessment (e.g., Low, Medium, High)
        2. Key Risk Factors identified (as a comma-separated list)
        3. Recommended Lifestyle Changes (as a comma-separated list)
        4. Symptoms to Monitor (as a comma-separated list)
        5. When to Visit a Doctor (as a comma-separated list)
        6. A numeric risk score (0-100).

        Format your response as a JSON object with the following keys: "risk_level", "risk_factors", "recommendations", "symptoms_to_monitor", "when_to_visit_doctor", "risk_score". Ensure 'risk_factors' and 'recommendations' are arrays of strings.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        llm_response_content = chat_completion.choices[0].message.content.strip()
        print(f"Raw LLM response content: {llm_response_content}") # DEBUG LOG
        
        # Use regex to robustly extract JSON string from LLM response
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', llm_response_content)
        if json_match:
            json_string = json_match.group(1).strip()
        else:
            json_string = llm_response_content # Fallback if no markdown block found

        # Parse the JSON response from the LLM
        try:
            parsed_response = json.loads(json_string)
            # Map LLM keys to RiskAnalysisStructuredResponse keys
            structured_response = RiskAnalysisStructuredResponse(
                risk_factors=parsed_response.get("risk_factors", []),
                risk_score=parsed_response.get("risk_score", 0),
                recommendations=parsed_response.get("recommendations", []),
                risk_level=parsed_response.get("risk_level", "Not assessed")
            )
            return structured_response
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse LLM response as JSON: {str(e)} - Response: {llm_response_content}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")

@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    try:
        # Helper function to format value
        def format_value(value):
            if isinstance(value, dict):
                return ", ".join(f"{k}: {v}" for k, v in value.items())
            elif isinstance(value, list):
                return ", ".join(str(item) for item in value)
            return str(value)

        # Generate the report sections
        report = {
            "report_id": f"REP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sections": {
                "patient_information": {
                    "title": "Patient Information",
                    "data": {k: format_value(v) for k, v in request.patient_info.items() if k != "additionalProp1"},
                    "additional_info": request.patient_info.get("additionalProp1", {})
                },
                "cancer_detection": {
                    "title": "Cancer Detection Result",
                    "data": {k: format_value(v) for k, v in request.cancer_result.items() if k != "additionalProp1"},
                    "additional_info": request.cancer_result.get("additionalProp1", {})
                }
            }
        }

        # Add risk analysis if available
        if request.risk_analysis:
            report["sections"]["risk_analysis"] = {
                "title": "Risk Analysis",
                "data": {
                    "risk_factors": ", ".join(request.risk_analysis.get("risk_factors", [])) if request.risk_analysis.get("risk_factors") else "Not assessed",
                    "risk_score": str(request.risk_analysis.get("risk_score", 0)),
                    "recommendations": ", ".join(request.risk_analysis.get("recommendations", [])) if request.risk_analysis.get("recommendations") else "Complete risk assessment required",
                    "risk_level": request.risk_analysis.get("risk_level", "Not assessed")
                },
                "additional_info": request.risk_analysis.get("additionalProp1", {})
            }

        # Add a summary section
        report["summary"] = {
            "status": "Complete",
            "key_findings": [
                f"Cancer Type: {request.cancer_result.get('prediction_text', 'Not detected')}",
                f"Confidence: {request.cancer_result.get('confidence', 'N/A')}",
                f"Risk Level: {request.risk_analysis.get('risk_level', 'Not assessed') if request.risk_analysis else 'Not assessed'}"
            ]
        }

        return JSONResponse(content=report)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@app.post("/educational-chat")
async def educational_chat(request: ChatMessage):
    try:
        prompt = f"""You are an educational AI assistant specializing in lung cancer.
        Provide clear, educational responses suitable for medical students.
        Include relevant medical terminology and explanations.
        
        User Question: {request.message}"""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        return {"response": chat_completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Educational chat failed: {str(e)}")
