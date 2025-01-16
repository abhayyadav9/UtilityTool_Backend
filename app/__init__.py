from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    CORS(app)
    

    # Register blueprints
    from app.routes.remove_background import remove_bg_bp
    from app.routes.qr_code import qr_code_bp
    from app.routes.greet import greet_bp
    from app.routes.doc_pdf import converter
    from app.routes.pdf_doc import pdf_converter
    from app.routes.enhance import image_enhancer
    from app.routes.resizer import image_resizer

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # Register blueprints with their unique names
    app.register_blueprint(greet_bp)
    app.register_blueprint(qr_code_bp)
    app.register_blueprint(remove_bg_bp)
    app.register_blueprint(converter, url_prefix='/converter')  # Registered with /converter
    app.register_blueprint(pdf_converter, url_prefix='/pdfconverter')
    app.register_blueprint(image_enhancer)
    app.register_blueprint(image_resizer)

    return app
