import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF4 import PdfFileReader, PdfFileWriter
import os
from io import BytesIO

# Assume previous functions (create_watermark and add_watermark) are defined here

def main():
    st.title("Frank's PDF Watermarker")

    # Check if the reset flag is set in the session state and if so, clear the uploaded file
    if 'reset' in st.session_state and st.session_state.reset:
        st.session_state.uploaded_file = None
        st.session_state.reset = False  # Reset the flag

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="uploaded_file")
    watermark_text = st.text_input("Watermark text", "Confidential")

    if uploaded_file is not None and watermark_text:
        # To read and save the uploaded file
        input_pdf = PdfFileReader(uploaded_file)

        # Create watermark PDF in memory
        watermark_pdf = BytesIO()
        create_watermark(input_pdf, watermark_pdf, watermark_text)
        watermark_pdf.seek(0)  # Move to the beginning of the StringIO buffer

        # Prepare output PDF path
        output_pdf_path = "watermarked_pdf.pdf"

        # Add watermark
        add_watermark(input_pdf, watermark_pdf, output_pdf_path)

        # Download link for watermarked PDF
        with open(output_pdf_path, "rb") as file:
            btn = st.download_button(
                label="Download watermarked PDF",
                data=file,
                file_name="watermarked_pdf.pdf",
                mime="application/pdf"
            )

    # Button to watermark another page
    if st.button("Watermark another page"):
        st.session_state.reset = True  # Set the reset flag
        st.experimental_rerun()

if __name__ == "__main__":
    if 'reset' not in st.session_state:
        st.session_state.reset = False  # Initialize reset flag
    main()
