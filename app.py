import streamlit as st
import requests
import base64
import os
from PIL import Image
from dotenv import load_dotenv
from config import GEMINI_API_ENDPOINT

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="🌱 Plant Disease Detection", layout="wide")

# Sidebar info
with st.sidebar:
    st.title("🌿 Plant Doctor Assistant")
    st.info("Upload a leaf image to detect disease & get care tips.")
    st.markdown("---")
    st.markdown("🔗 [GitHub](https://github.com/your_repo)")
    st.markdown("📬 Contact: your.email@example.com")

st.title("🌾 Plant Disease Detection")
st.markdown("Upload a leaf photo to identify diseases 🌿")
uploaded_file = st.file_uploader("📷 Upload leaf image", type=["jpg", "jpeg", "png"])

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def get_gemini_analysis(encoded_image):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [
                {"text": "Analyze this plant leaf image and identify any diseases, symptoms, and care suggestions."},
                {"inlineData": {"mimeType": "image/jpeg", "data": encoded_image}}
            ]
        }]
    }
    response = requests.post(
        f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

if uploaded_file:
    image_bytes = uploaded_file.read()
    encoded_image = encode_image(image_bytes)
    st.image(uploaded_file, caption="Uploaded Leaf", use_column_width=True)

    with st.spinner("Analyzing..."):
        try:
            result = get_gemini_analysis(encoded_image)
            st.success("Analysis Complete!")
            st.markdown("### 🧬 Result:")
            st.markdown(result)
        except Exception as e:
            st.error("Something went wrong. Check API key or image format.")