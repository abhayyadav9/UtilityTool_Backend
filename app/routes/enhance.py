from flask import Blueprint, Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2

# Define the blueprint
image_enhancer = Blueprint('enhance', __name__)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload and enhancement
@image_enhancer.route('/enhance', methods=['POST'])
def enhance_image():
    # Check if a file was uploaded
    print("file received")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        try:
            # Enhance Image
            enhanced_image_path = enhance_image_quality(filepath)
            # Send the enhanced image back to the client
            return send_file(enhanced_image_path, as_attachment=True, download_name="enhanced_image.png", mimetype="image/png")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file format"}), 400

def enhance_image_quality(image_path):
    enhanced_image_path = image_path.rsplit('.', 1)[0] + '_enhanced.png'
    
    # Load the image
    img = cv2.imread(image_path)
    
    # Enhance the image (increase brightness and contrast)
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 50    # Brightness control (0-100)

    enhanced_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    
    # Save the enhanced image
    cv2.imwrite(enhanced_image_path, enhanced_img)
    
    return enhanced_image_path
