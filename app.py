import streamlit as st
import requests
from PIL import Image
import io
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾")

# Custom CSS for modern UI
custom_css = """
<style>
.main {
    background: linear-gradient(135deg, #f4faff, #eaf6ff);
}
.upload-container {
    text-align: center;
    border: 2px dashed #4aa3f0;
    padding: 20px;
    border-radius: 15px;
    background: white;
}
.result-box {
    padding: 20px;
    border-radius: 15px;
    background: #ffffffcc;
    backdrop-filter: blur(10px);
    text-align: center;
    font-size: 22px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("🐱🐶 Cat vs Dog Classifier")

CAT_LOTTIE = "https://assets2.lottiefiles.com/private_files/lf30_editor_jckcic9a.json"
DOG_LOTTIE = "https://assets2.lottiefiles.com/private_files/lf30_ud5z4j5o.json"
LOADING_LOTTIE = "https://assets10.lottiefiles.com/packages/lf20_YXD37q.json"

def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json()
    except:
        return None

API_URL = "https://asdjbfag-cat-dog-classification.hf.space/predict"
headers = {}

st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    if st.button("🚀 Predict Now", use_container_width=True):
        with st.spinner("AI is analyzing the image... 🧠🐾"):
            st_lottie(load_lottie(LOADING_LOTTIE), height=200)

            files = {"file": ("image.png", img_bytes, "image/png")}
            try:
                response = requests.post(API_URL, headers=headers, files=files, timeout=30)
                raw_text = response.text

                # Ambil JSON valid di dalam response
                json_start = raw_text.find("{")
                json_end = raw_text.rfind("}") + 1
                json_str = raw_text[json_start:json_end]

                result = json.loads(json_str)
                prediction = result.get("prediction", "Unknown")

                st.subheader("🔍 Prediction Result")
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)

                if prediction.lower() == "cat":
                    st.success("🐱 It's a CAT!")
                    st_lottie(load_lottie(CAT_LOTTIE), height=200)
                else:
                    st.success("🐶 It's a DOG!")
                    st_lottie(load_lottie(DOG_LOTTIE), height=200)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("🚨 Error processing request!")
                st.write(raw_text)
                st.text(str(e))
