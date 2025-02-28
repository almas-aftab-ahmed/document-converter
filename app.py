import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for PDFs
from io import BytesIO
from docx import Document

def convert_pdf_to_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

def convert_docx_to_text(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def convert_csv_to_excel(csv_file):
    df = pd.read_csv(csv_file)
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    return output

# Custom CSS for Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            text-align: center;
        }
        .stButton>button {
            background: #ff9800;
            color: white;
            border-radius: 10px;
            font-size: 18px;
        }
        .stFileUploader {
            background: white;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Documents Converter")
st.markdown("Convert your files easily and download them instantly! 🚀")

uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "csv"], help="Supported formats: PDF, DOCX, TXT, CSV")
if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    st.success(f"Uploaded file: {uploaded_file.name}")
    st.markdown("### Processing file... ⏳")
    
    if file_extension == "pdf":
        text = convert_pdf_to_text(uploaded_file)
        st.download_button("📥 Download TXT", text, file_name="converted.txt", key="pdf")
    elif file_extension == "docx":
        text = convert_docx_to_text(uploaded_file)
        st.download_button("📥 Download TXT", text, file_name="converted.txt", key="docx")
    elif file_extension == "csv":
        excel_file = convert_csv_to_excel(uploaded_file)
        st.download_button("📥 Download Excel", excel_file, file_name="converted.xlsx", key="csv")
    elif file_extension == "txt":
        text = uploaded_file.read().decode("utf-8")
        st.download_button("📥 Download TXT", text, file_name="converted.txt", key="txt")
    else:
        st.error("❌ Unsupported file type! Please upload a valid format.")
