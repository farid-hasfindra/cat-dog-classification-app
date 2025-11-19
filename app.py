import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾")

st.title("🐱🐶 Cat vs Dog Classifier")

# URL API inference Hugging Face (ubah sesuai modelmu)
API_URL = "https://cat-dog-classification.asdjbfag.hf.space/predict"

# Jika endpoint butuh autentikasi tambahkan token kamu
headers = {"Authorization": "Bearer HF_API_KEY"}  # isi tokenmu
# Jika tidak perlu token, ubah jadi:
# headers = {}

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Uploaded Image", width='stretch')
    
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    if st.button("Predict"):
        with st.spinner("Analyzing the image..."):
            response = requests.post(API_URL, headers=headers, data=img_bytes)

            if response.status_code == 200:
                result = response.json()

                # HuggingFace biasanya memberi list dict: [{"label": "...", "score": ...}]
                label = result[0]['label']
                score = result[0]['score'] * 100

                with col2:
                    st.subheader("Prediction Result")
                    st.success(f"**{label}** ({score:.2f}% confidence)")

            else:
                st.error("Error processing request!")
                st.write(response.text)
