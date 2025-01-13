import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Backend is running successfully!"

    return app

app = create_app()

if __name__ == "__main__":
    # Use the port from the environment or default to 5000
    # port = int(os.environ.get("PORT", 5000))  # Ensure the port is dynamically set
    app.run(host='0.0.0.0', port=5000)
