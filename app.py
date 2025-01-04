import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import fitz
from PIL import Image
import io

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def pdf_to_images_list(pdf_file):
    images = []
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page_number in range(len(doc)):
            page = doc[page_number]
            pix = page.get_pixmap()
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            images.append(image)
    return images


def image_details(image):
    if image is not None:
        with io.BytesIO() as buffer:
            image.save(buffer, format="PNG")
            bytes_data = buffer.getvalue()
        images = {
            "mime_type": "image/png",
            "data": bytes_data
        }
        return images
    else:
        raise ValueError("No Image Found")


def pdf_to_image_data(pdf):
    images = pdf_to_images_list(pdf)
    details = [image_details(img) for img in images]
    return details


def get_response(input_prompt, images):
    try:
        response = model.generate_content([input_prompt, *images])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


# ------------------UI---------------------

st.set_page_config(page_title="Invoice Extraction")
st.header("Invoice Extraction")
uploaded_file = st.file_uploader("Upload the invoice", type=["pdf"])
input_prompts = "You are an expert in understanding invoices. We will upload images as single invoice and you have to extract the data. Show it. Data which is in tabular form , show it in table form . Don't add introduction and conclusion"

submit_button = st.button("Submit")
if submit_button:
    details = pdf_to_image_data(uploaded_file)
    result = get_response(input_prompts, details)
    st.write(result)
