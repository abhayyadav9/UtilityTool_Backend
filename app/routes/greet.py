from flask import Blueprint, request, jsonify

greet_bp = Blueprint('greet', __name__)

@greet_bp.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    greeting = f"Hello, {name}!"
    return jsonify({'greeting': greeting})
