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
    from app.routes.doc_convert import doc_convert_bp
    from app.routes.doc_pdf import converter

    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

    # Register blueprints with their unique names
    app.register_blueprint(qr_code_bp, url_prefix='/qr_code')
    app.register_blueprint(converter, url_prefix='/converter')  # Registered with /converter
    app.register_blueprint(remove_bg_bp)
    app.register_blueprint(greet_bp)
    app.register_blueprint(doc_convert_bp)

    return app
