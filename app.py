import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

model = genai.GenerativeModel("gemini-1.0-pro-latest")

# ------------------UI---------------------

st.set_page_config(page_title="Invoice Extraction")
st.header("Invoice Extraction")
uploaded_file = st.file_uploader("Upload the invoice", type=["pdf"])
