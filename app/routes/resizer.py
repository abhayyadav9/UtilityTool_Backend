from flask import Flask, Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2


image_resizer = Blueprint('resize', __name__)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload and resizing
@image_resizer.route('/resize', methods=['POST'])
def resize_image():
    print("Request received")
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
            # Resize Image
            resized_image_path = resize_image_quality(filepath)
            # Send the resized image back to the client
            return send_file(resized_image_path, as_attachment=True, download_name="resized_image.jpg", mimetype="image/jpeg")
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "Invalid file format"}), 400

def resize_image_quality(image_path):
    resized_image_path = image_path.rsplit('.', 1)[0] + '_resized.jpg'
    
    # Load the image
    img = cv2.imread(image_path)
    
    # Get the current dimensions
    height, width = img.shape[:2]
    
    # Scale factor (reduce size by 50%)
    scale_factor = 0.5
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Resize the image while maintaining the aspect ratio
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    # Save the resized image with JPEG format to reduce the file size further
    cv2.imwrite(resized_image_path, resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    
    return resized_image_path

