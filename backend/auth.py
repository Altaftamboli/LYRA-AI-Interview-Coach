from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


# Register User
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration Successful"}), 201


# Login User
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify(
            {"message": "Login Successful", "user_id": user.id, "name": user.name}
        )

    return jsonify({"message": "Invalid Email or Password"}), 401
