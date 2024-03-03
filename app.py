import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import PyPDF4
import os
from io import BytesIO

def create_watermark(output_file_path, text="Confidential"):
    """
    Creates a watermark PDF with specified text.
    """
    st.write("Creating watermark...")
    c = canvas.Canvas(output_file_path, pagesize=letter)
    c.setFont("Helvetica", 60)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)  # Semi-transparent grey
    c.saveState()
    c.translate(500, 100)  # Bottom right
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    st.write("Watermark created.")

def add_watermark(input_pdf, watermark_pdf, output_pdf_path):
    """
    Adds the created watermark to all pages of the input PDF.
    """
    st.write(f"Adding watermark...")
    watermark_pdf = PyPDF4.PdfFileReader(watermark_pdf)
    watermark_page = watermark_pdf.getPage(0)

    output_pdf = PyPDF4.PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(i)
        page.mergePage(watermark_page)
        output_pdf.addPage(page)

    with open(output_pdf_path, "wb") as output_pdf_file:
        output_pdf.write(output_pdf_file)
    st.write("Watermark added successfully.")

def main():
    st.title('PDF Watermarker')

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    watermark_text = st.text_input("Watermark text", "Confidential")
    if uploaded_file is not None and watermark_text:
        # To read and save the uploaded file
        input_pdf = PyPDF4.PdfFileReader(uploaded_file)

        # Create watermark PDF in memory
        watermark_pdf = BytesIO()
        create_watermark(watermark_pdf, watermark_text)
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

if __name__ == "__main__":
    main()
