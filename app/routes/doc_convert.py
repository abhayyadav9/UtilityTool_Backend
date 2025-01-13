from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
import os
from docx import Document
from pdf2docx import Converter
from PyPDF2 import PdfReader

doc_convert_bp = Blueprint("doc_convert", __name__)

@doc_convert_bp.route('/convert/docx-to-pdf', methods=['POST'])
def convert_docx_to_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if not file.filename.endswith('.docx'):
            return jsonify({'error': 'Invalid file type. Only .docx files are supported.'}), 400

        # Load the .docx file
        doc = Document(file)

        # Placeholder logic (python-docx cannot directly convert to PDF)
        # Save the .docx to a temporary file (for later use in conversion)
        temp_docx = "temp.docx"
        doc.save(temp_docx)

        # Convert .docx to PDF using a third-party tool (e.g., LibreOffice, pypdf2, or API)
        # For now, you need a library like `unoconv` or integrate with an online tool
        # Raise an error here if unsupported
        os.remove(temp_docx)
        return jsonify({'error': 'DOCX to PDF conversion is not yet implemented.'}), 501

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doc_convert_bp.route('/convert/pdf-to-docx', methods=['POST'])
def convert_pdf_to_docx():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Only .pdf files are supported.'}), 400

        # Save the PDF to a temporary file
        temp_pdf = "temp.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(file.read())

        # Convert the PDF to DOCX using pdf2docx
        temp_docx = "output.docx"
        converter = Converter(temp_pdf)
        converter.convert(temp_docx, start=0, end=None)
        converter.close()

        # Read the DOCX file back into memory
        with open(temp_docx, "rb") as f:
            docx_data = f.read()

        # Clean up temporary files
        os.remove(temp_pdf)
        os.remove(temp_docx)

        # Return the converted DOCX file
        return send_file(BytesIO(docx_data), mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document", as_attachment=True, download_name="converted.docx")

    except Exception as e:
        return jsonify({'error': str(e)}), 500
