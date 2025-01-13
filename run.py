from flask import Flask

def create_app():
    app = Flask(__name__)

    # Simple route to confirm backend is running
    @app.route('/')
    def home():
        return "Backend is running successfully!"

    return app

app = create_app()  # Gunicorn looks for this "app"

# Uncomment the following line if you want to run it locally
# if __name__ == '__main__':
#     app.run(debug=True)
