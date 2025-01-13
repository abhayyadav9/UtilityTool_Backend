import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hello Abhay.. Your backend is running"

    return app

app = create_app()

if __name__ == "__main__":
    # Use the port from the environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
