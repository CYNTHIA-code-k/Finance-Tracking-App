from flask import request, jsonify
from app.routes import auth_bp
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
