from io import BytesIO
from docx import Document
from pdf2docx import Converter
import os
from fpdf import FPDF


def docx_to_pdf(docx_file):
    """Convert DOCX to PDF and return the PDF as a BytesIO buffer."""
    document = Document(docx_file)
    buffer = BytesIO()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for paragraph in document.paragraphs:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(190, 10, txt=paragraph.text)

    pdf.output(buffer)
    buffer.seek(0)
    return buffer


def pdf_to_docx(pdf_file):
    """Convert PDF to DOCX and return the DOCX as a BytesIO buffer."""
    buffer = BytesIO()
    temp_pdf_path = "temp.pdf"
    temp_docx_path = "temp.docx"

    # Save the uploaded file temporarily
    with open(temp_pdf_path, 'wb') as f:
        f.write(pdf_file.read())

    # Convert PDF to DOCX
    cv = Converter(temp_pdf_path)
    cv.convert(temp_docx_path, start=0, end=None)
    cv.close()

    # Read the converted DOCX
    with open(temp_docx_path, 'rb') as f:
        buffer.write(f.read())

    # Cleanup temporary files
    os.remove(temp_pdf_path)
    os.remove(temp_docx_path)

    buffer.seek(0)
    return buffer
