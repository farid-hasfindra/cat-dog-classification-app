import streamlit as st
import requests
from PIL import Image
import io
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾", layout="centered")

# Custom UI Styles
st.markdown("""
<style>
.main { background: linear-gradient(135deg, #f4faff, #eaf6ff); }
.upload-container {
    text-align: center;
    border: 2px dashed #4aa3f0;
    padding: 20px;
    border-radius: 15px;
    background: #ffffffcc;
    margin-bottom: 20px;
}
.result-box {
    margin-top: 20px;
    padding: 20px;
    border-radius: 15px;
    background: #ffffffcc;
    text-align: center;
    font-size: 22px;
}
.center {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🐱🐶 Cat vs Dog Classifier")

# Safe animation loading
def load_lottie(url):
    try:
        r = requests.get(url, timeout=8)
        data = r.json()
        if isinstance(data, dict):
            return data
    except:
        return None

CAT_LOTTIE = load_lottie("https://lottie.host/5cd0bddd-122f-4cab-bde5-8a67fe93a9f5/BUD2zmNwVt.json")
DOG_LOTTIE = load_lottie("https://lottie.host/9da15633-31d8-477a-b52c-e43efc3fea6b/0J5ZJRU1S0.json")

API_URL = "https://asdjbfag-cat-dog-classification.hf.space/predict"
headers = {}

# Upload UI
st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])
st.markdown("</div>", unsafe_allow_html=True)

# Display image + button
if uploaded_file:
    image = Image.open(uploaded_file)

    # Center + Smaller Size 👌
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    st.image(image, caption="Uploaded Image", width=300)
    st.markdown("</div>", unsafe_allow_html=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    # Predict Button
    if st.button("🚀 Predict Now", use_container_width=True):
        with st.spinner("AI is analyzing the image... 🧠🐾"):

            try:
                response = requests.post(API_URL, headers=headers,
                                         files={"file": ("image.png", img_bytes, "image/png")})
                raw_text = response.text

                # Clean JSON extract
                json_start = raw_text.find("{")
                json_end = raw_text.rfind("}") + 1
                result = json.loads(raw_text[json_start:json_end])

                prediction = result.get("prediction", "unknown").lower()

                st.subheader("🔍 Prediction Result")
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)

                if prediction == "cat":
                    st.success("🐱 It's a CAT!")
                    if CAT_LOTTIE: st_lottie(CAT_LOTTIE, height=200)
                else:
                    st.success("🐶 It's a DOG!")
                    if DOG_LOTTIE: st_lottie(DOG_LOTTIE, height=200)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("🚨 Error processing request!")
                st.text(str(e))
                st.write(raw_text)
                
                