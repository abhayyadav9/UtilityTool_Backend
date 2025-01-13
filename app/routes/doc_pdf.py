from flask import Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pythoncom
from win32com import client

# Define the blueprint
converter = Blueprint('doc_pdf_converter', __name__)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'docx'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload and conversion
@converter.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    print(file)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), 'uploads')  # Path for uploads
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        try:
            # Convert DOCX to PDF
            pdf_path = convert_docx_to_pdf(filepath)
            # Send the converted PDF file back to the client
            return send_file(pdf_path, as_attachment=True, download_name="converted_file.pdf", mimetype="application/pdf")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Invalid file format"}), 400

# Function to convert DOCX to PDF
def convert_docx_to_pdf(docx_path):
    pythoncom.CoInitialize()
    word = client.Dispatch("Word.Application")
    doc = word.Documents.Open(docx_path)
    pdf_path = docx_path.rsplit('.', 1)[0] + '.pdf'
    doc.SaveAs(pdf_path, FileFormat=17)  # 17 represents the PDF format
    doc.Close()
    word.Quit()
    return pdf_path
