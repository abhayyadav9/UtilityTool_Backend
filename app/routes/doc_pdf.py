from flask import Flask, Blueprint, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pypandoc


# Define the blueprint
converter = Blueprint('doc_pdf_converter', __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'docx'}

# Upload folder setup
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload and conversion
@converter.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Convert DOCX to PDF
            pdf_path = convert_docx_to_pdf(filepath)
            return send_file(pdf_path, as_attachment=True, download_name="converted_file.pdf", mimetype="application/pdf")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file format"}), 400

# Function to convert DOCX to PDF using Pandoc
def convert_docx_to_pdf(docx_path):
    pdf_path = docx_path.rsplit('.', 1)[0] + '.pdf'
    output = pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path)
    if output:
        print("Conversion output:", output)  # Debugging log
    return pdf_path

