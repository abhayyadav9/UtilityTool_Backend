from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from PIL import Image
import rembg

remove_bg_bp = Blueprint('remove_bg', __name__)

@remove_bg_bp.route('/remove-background', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        input_image = file.read()
        output_image = rembg.remove(input_image)
        img = Image.open(BytesIO(output_image))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
