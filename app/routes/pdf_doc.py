


import os
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF

# Define the blueprint
pdf_converter = Blueprint('pdf_doc_converter', __name__)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload and conversion
@pdf_converter.route('/pdfdoc', methods=['POST'])
def convert_pdf_to_docx():
    print("Request received")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), 'uploads')  # Path for uploads
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        try:
            # Convert PDF to DOCX
            docx_path = convert_pdf_to_docx(filepath)
            # Send the converted DOCX file back to the client
            return send_file(docx_path, as_attachment=True, download_name="converted_file.docx", mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file format"}), 400

def convert_pdf_to_docx(pdf_path):
    try:
        print(f"Converting PDF: {pdf_path}")
        docx_path = pdf_path.rsplit('.', 1)[0] + '.docx'
        
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        
        # Create a new DOCX file
        from docx import Document
        doc = Document()
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text")
            doc.add_paragraph(text)
        
        doc.save(docx_path)
        
        print(f"Conversion successful: {docx_path}")
        return docx_path
    except Exception as e:
        print("Error during conversion:", e)
        raise

