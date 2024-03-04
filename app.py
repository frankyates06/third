import streamlit as st
from reportlab.pdfgen import canvas
from PyPDF4 import PdfFileReader, PdfFileWriter
from io import BytesIO

def create_watermark(input_pdf, text="Confidential"):
    """
    Creates a watermark PDF with specified text, matching the size of the input PDF's first page.
    Returns a BytesIO object containing the watermark PDF.
    """
    page = input_pdf.getPage(0)
    page_size = page.mediaBox
    watermark_pdf = BytesIO()
    c = canvas.Canvas(watermark_pdf, pagesize=(page_size[2], page_size[3]))
    c.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.5)  # Less pale grey
    c.setFont("Helvetica", 12)  # Font size 12

    # Repeat the watermark text as a pattern
    text_width = c.stringWidth(text, "Helvetica", 12)
    for x in range(0, int(page_size[2]), int(text_width) + 60):  # Adjust spacing based on your preference
        for y in range(0, int(page_size[3]), 60):  # Adjust vertical spacing
            c.saveState()
            c.translate(x, y)
            c.drawCentredString(0, 0, text)
            c.restoreState()

    c.save()
    watermark_pdf.seek(0)  # Move to the beginning of the BytesIO buffer
    return watermark_pdf

def add_watermark(input_pdf, watermark_pdf):
    """
    Adds the created watermark to all pages of the input PDF.
    Returns a BytesIO object containing the watermarked PDF.
    """
    watermark = PdfFileReader(watermark_pdf)
    watermark_page = watermark.getPage(0)

    output_pdf = PdfFileWriter()

    for i in range(input_pdf.getNumPages()):
        page = input_pdf.getPage(i)
        page.mergePage(watermark_page)
        output_pdf.addPage(page)

    output_pdf_stream = BytesIO()
    output_pdf.write(output_pdf_stream)
    output_pdf_stream.seek(0)
    return output_pdf_stream

def main():
    st.title("Frank's PDF Watermarker")

    if 'reset' not in st.session_state or st.session_state.reset:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="uploaded_file")
        watermark_text = st.text_input("Watermark text", "Confidential", key="watermark_text")

    if st.button("Watermark another page"):
        # This will clear the session state and refresh the page
        for key in st.session_state.keys():
            del st.session_state[key]
        st.session_state.reset = True
        st.experimental_rerun()

    # Move the download button to the front
    if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None and st.session_state.watermark_text:

        input_pdf = PdfFileReader(st.session_state.uploaded_file)
        watermark_pdf = create_watermark(input_pdf, st.session_state.watermark_text)
        watermarked_pdf = add_watermark(input_pdf, watermark_pdf)

        # Customize the download button
        st.download_button(
            label="Download watermarked PDF",
            data=watermarked_pdf,
            file_name="watermarked_pdf.pdf",
            mime="application/pdf",
            key="download-button",
            style="background-color: red; color: white;",
            icon="bi bi-download",
        )

if __name__ == "__main__":
    main()