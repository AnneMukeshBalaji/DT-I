import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure your Gemini API Key
genai.configure(api_key="AIzaSyAgTNJvgpgKWVgNU9y0kZcCaaB9BHZ6Vow")  # Replace with your actual key

# Load the correct image-supported model
model = genai.GenerativeModel(model_name="models/gemini-pro-vision")

# Streamlit UI setup
st.set_page_config(page_title="Payment Status Checker", layout="centered")
st.title("💳 Payment Status Checker")
st.write("Upload an image to check if a payment is being made or not.")

# Upload section
uploaded_file = st.file_uploader("📸 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🔍 Analyze"):
        with st.spinner("Analyzing image with Gemini..."):
            try:
                prompt = """
This image was captured during a payment interaction. Your task is to analyze and determine if:
1. The image shows someone scanning a QR code,
2. There's a payment confirmation screen, or
3. A POS machine is being used.

Reply strictly with only:
- Payment Done
- Payment Not Done
"""

                response = model.generate_content(
                    contents=[prompt, image],
                    stream=False
                )

                result = response.text.strip()
                st.success(f"✅ Gemini Response: **{result}**")

            except Exception as e:
                st.error(f"❌ Error: {e}")
