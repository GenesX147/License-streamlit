import streamlit as st
import pytesseract as pt
from PIL import Image, ImageDraw
import pandas as pd

pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("License Plate With OCR")

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    d = pt.image_to_data(img, lang='tha', output_type=pt.Output.DICT, config='--psm 11 --oem 1')
    df = pd.DataFrame.from_dict(d)
    df_filtered = df[df.conf.astype(int) > 60]
    draw = ImageDraw.Draw(img)
    for i in range(len(df_filtered)):
        if int(df_filtered.iloc[i]['conf']) > 60:
            x, y, w, h = df_filtered.iloc[i]['left'], df_filtered.iloc[i]['top'], df_filtered.iloc[i]['width'], df_filtered.iloc[i]['height']
            draw.rectangle(((x, y), (x + w, y + h)), outline="red", width=2)
    st.image(img, caption='Uploaded Image with Detected Text', use_column_width=True)
    st.write("OCR Result:")
    st.dataframe(df_filtered[['text', 'conf', 'left', 'top', 'width', 'height']])
    for i in range(len(df_filtered)):
        if int(df_filtered.iloc[i]['conf']) > 60:
            text = df_filtered.iloc[i]['text']
            st.write(f"Text: {text} (Confidence: {df_filtered.iloc[i]['conf']})")
else:
    st.write("Please upload an image file")
