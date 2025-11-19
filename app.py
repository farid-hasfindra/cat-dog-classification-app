import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾")

st.title("🐱🐶 Cat vs Dog Classifier")

# URL API inference Hugging Face (update sesuai endpoint-mu)
API_URL = "https://asdjbfag-cat-dog-classification.hf.space/predict"

# Jika tidak butuh token, kosongkan jadi {}
headers = {}

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    if st.button("Predict"):
        with st.spinner("Analyzing the image..."):
            files = {
                "file": ("uploaded.png", img_bytes, "image/png")
            }

            try:
                response = requests.post(API_URL, headers=headers, files=files, timeout=30)
                response.raise_for_status()

                result = response.json()

                # Sesuaikan format JSON API Hugging Face: [{"label": "...", "score": ...}]
                label = result[0].get("label", "Unknown")
                score = result[0].get("score", 0.0) * 100

                with col2:
                    st.subheader("Prediction Result")
                    st.success(f"**{label}** ({score:.2f}% confidence)")

            except Exception as e:
                st.error("Error processing request!")
                st.text(str(e))
                st.write(response.text if 'response' in locals() else "")
