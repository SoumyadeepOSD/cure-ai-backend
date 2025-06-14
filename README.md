---
title: Lung Cancer
emoji: 🌖
colorFrom: red
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: It's a vgg16 model of predicting lung cancer from images
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
# lung-cancer-backend
# lung-cancer-backend
# cure-ai-backend

# Lung Cancer Detection System

## Required Packages

### Backend Dependencies
```python
# Web Framework and Server
fastapi==0.109.2        # Modern web framework for building APIs
uvicorn==0.27.1         # ASGI server for running FastAPI applications

# Image Processing
pillow==10.2.0         # Python Imaging Library for image manipulation
numpy==1.26.4          # Numerical computing library

# Machine Learning
tensorflow==2.15.0     # Deep learning framework for VGG16 model
torch==2.2.0           # PyTorch for additional ML capabilities
transformers==4.37.2   # Hugging Face Transformers library

# AI and Language Models
langchain==0.1.4       # Framework for LLM applications
langchain-google-genai==0.0.5  # Google's Gemini integration
groq==0.4.2            # Groq LLM API client
huggingface_hub==0.20.3  # Hugging Face model hub integration

# Utilities
python-dotenv==1.0.1   # Environment variable management
httpx==0.26.0          # Async HTTP client
python-multipart==0.0.6  # Multipart form data parsing
reportlab==4.0.9       # PDF generation library
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "@emotion/react": "^11.11.3",    // CSS-in-JS styling
    "@emotion/styled": "^11.11.0",   // Styled components
    "@mui/material": "^5.15.10",     // Material UI components
    "@mui/icons-material": "^5.15.10", // Material UI icons
    "react": "^18.2.0",              // React core
    "react-dom": "^18.2.0",          // React DOM
    "react-router-dom": "^6.22.1",   // React routing
    "react-scripts": "5.0.1"         // React development scripts
  }
}
```

### Installation Instructions
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Environment Variables
Create a `.env` file in the root directory with:
```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

## System Architecture Pseudocode

![System Workflow Diagram]({B7E4AE99-083C-40A5-8FFD-BC6A77C65D1C}.png) %% REPLACE THIS WITH THE ACTUAL IMAGE PATH

### 1. Backend API (FastAPI)
```