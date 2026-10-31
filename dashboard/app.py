import pandas as pd
import streamlit as st
from PIL import Image
from ultralytics import YOLO

MODEL_PATH = "runs/detect/experiments/baseline_v2/weights/best.pt"

st.set_page_config(page_title="Marine Biodiversity AI", page_icon="🌊")
st.title("🌊 Marine Biodiversity AI")
st.write("Upload a deep-sea photo and the model will try to find and name the animals. "
         "It knows 20 animal types from the FathomNet dataset.")

@st.cache_resource            # load the model only once
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

conf = st.slider("Minimum confidence", 0.05, 0.9, 0.25, 0.05,
                 help="Higher = fewer boxes, but more of them are right.")

file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if file is not None:
    image = Image.open(file).convert("RGB")
    result = model.predict(image, imgsz=416, conf=conf, device="cpu", verbose=False)[0]

    # result.plot() returns BGR, so flip to RGB for display
    st.image(result.plot()[:, :, ::-1], caption="Model predictions", use_container_width=True)

    names = [result.names[int(c)] for c in result.boxes.cls]
    if names:
        counts = pd.Series(names).value_counts().rename_axis("Animal").reset_index(name="Count")
        st.subheader(f"Found {len(names)} animals")
        st.dataframe(counts, hide_index=True)
    else:
        st.info("No animals found at this confidence level. Try lowering the slider.")