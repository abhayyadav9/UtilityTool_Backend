from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from PIL import Image
import qrcode

qr_code_bp = Blueprint('qr_code', __name__)

@qr_code_bp.route('/generate-qr', methods=['POST'])
def create_qr():
    try:
        data_type = request.form.get('type', 'text')
        if data_type == 'image':
            if 'image' not in request.files:
                return jsonify({'error': 'No image file uploaded'}), 400
            image_file = request.files['image']
            image = Image.open(image_file)
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data('Custom QR Data')
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
            qr_image.thumbnail((100, 100))
            image.paste(qr_image, (0, 0), qr_image)
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return send_file(buffer, mimetype='image/png')
        elif data_type in ['link', 'text']:
            content = request.form.get('content')
            if not content:
                return jsonify({'error': 'No content provided'}), 400
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(content)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="green", back_color="black")
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            buffer.seek(0)
            return send_file(buffer, mimetype='image/png')
        else:
            return jsonify({'error': 'Invalid type parameter'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
