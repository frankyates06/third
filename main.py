import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import PyPDF4

def create_watermark(output_file_path, text="Confidential"):
    """
    Creates a watermark PDF with specified text.
    """
    print("Creating watermark...")
    c = canvas.Canvas(output_file_path, pagesize=letter)
    c.setFont("Helvetica", 60)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.5)  # Semi-transparent grey
    c.saveState()
    c.translate(500, 100)  # Bottom right
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    print("Watermark created.")

def add_watermark(input_pdf_path, watermark_pdf_path, output_pdf_path):
    """
    Adds the created watermark to all pages of the input PDF.
    """
    print(f"Adding watermark to {input_pdf_path}...")
    with open(input_pdf_path, "rb") as input_pdf_file, open(watermark_pdf_path, "rb") as watermark_pdf_file:
        input_pdf = PyPDF4.PdfFileReader(input_pdf_file)
        watermark_pdf = PyPDF4.PdfFileReader(watermark_pdf_file)
        watermark_page = watermark_pdf.getPage(0)

        output_pdf = PyPDF4.PdfFileWriter()

        for i in range(input_pdf.getNumPages()):
            page = input_pdf.getPage(i)
            page.mergePage(watermark_page)
            output_pdf.addPage(page)

        with open(output_pdf_path, "wb") as output_pdf_file:
            output_pdf.write(output_pdf_file)
    print("Watermark added successfully.")

def main():
    pdf_folder = "PDF"
    watermark_text = "Confidential"
    watermark_pdf_path = os.path.join(pdf_folder, "watermark.pdf")

    # Step 1: Create a watermark PDF
    create_watermark(watermark_pdf_path, watermark_text)

    # Step 2: Find a PDF file in the folder to watermark
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf") and not f.startswith("watermarked_")]
    if not pdf_files:
        print("No PDF files found to watermark.")
        return

    # Assuming we watermark the first PDF found
    input_pdf_path = os.path.join(pdf_folder, pdf_files[0])
    output_pdf_path = os.path.join(pdf_folder, f"watermarked_{pdf_files[0]}")

    # Step 3: Add watermark to the found PDF file
    add_watermark(input_pdf_path, watermark_pdf_path, output_pdf_path)

if __name__ == "__main__":
    main()
