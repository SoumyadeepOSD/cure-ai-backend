

import os
import io
import base64
from PIL import Image
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv(".env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is not set. Please set it in your .env file or environment.")


def pil_image_to_base64(image: Image.Image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def analyze_cancer_image(image_bytes: bytes, image_description: str = "Lung X-ray or CT scan image"):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_b64 = pil_image_to_base64(image)

        prompt_template = PromptTemplate(
            input_variables=["image_description"],
            template="""
You are a medical imaging expert. Given a lung cancer image, provide:

1. Stage of abnormality (early/late/none).
2. Signs of benign or malignant features.
3. Reasoning for your diagnosis.

Image Description: {image_description}
"""
        )
        final_prompt = prompt_template.format(image_description=image_description)

        # Initialize llm WITHOUT passing google_api_key parameter,
        # the library will use the environment variable GOOGLE_API_KEY automatically
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.4, google_api_key=GOOGLE_API_KEY)

        messages = [
            HumanMessage(
                content=[
                    {"type": "text", "text": final_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    }
                ]
            )
        ]

        response = llm.invoke(messages)
        return {"analysis": response.content}

    except Exception as e:
        return {"error": str(e)}
