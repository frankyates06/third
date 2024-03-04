import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF4 import PdfFileReader, PdfFileWriter
import os
from io import BytesIO

def create_watermark(input_pdf, output_file_path, text="Confidential"):
    """
    Creates a watermark PDF with specified text, matching the size of the input PDF's first page.
    """
    st.write("Creating watermark...")
    page = input_pdf.getPage(0)
    page_size = page.mediaBox

    c = canvas.Canvas(output_file_path, pagesize=(page_size[2], page_size[3]))
    c.setFillColorRGB(0.95, 0.95, 0.95, alpha=0.5)  # Very pale grey
    c.setFont("Helvetica", 10)  # Very small font

    # Repeat the watermark text as a pattern
    text_width = c.stringWidth(text, "Helvetica", 5)
    for x in range(0, int(page_size[2]), int(text_width) + 20):  # Adjust spacing based on your preference
        for y in range(0, int(page_size[3]), 20):  # Adjust vertical spacing
            c.saveState()
            c.translate(x, y)
            c.drawCentredString(0, 0, text)
            c.restoreState()

    c.save()
    st.write("Watermark created.")

def add_watermark(input_pdf, watermark_pdf, output_pdf_path):
    """
    Adds the created watermark to all pages of the input PDF.
    """
    st.write("Adding watermark...")
    watermark_pdf = PdfFileReader(watermark_pdf)
    watermark_page = watermark_pdf.getPage(0)

    output_pdf = PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(i)
        page.mergePage(watermark_page)
        output_pdf.addPage(page)

    with open(output_pdf_path, "wb") as output_pdf_file:
        output_pdf.write(output_pdf_file)
    st.write("Watermark added successfully.")

def main():
    st.title('Frank\'s PDF Watermarker ')

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
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
            st.experimental_rerun()

if __name__ == "__main__":
    main()
