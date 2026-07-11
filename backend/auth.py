from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import get_db_connection

auth_bp = Blueprint("auth", __name__)


# ------------------ Register ------------------ #
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        cursor.close()
        conn.close()
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
        (name, email, hashed_password),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Registration Successful"}), 201


# ------------------ Login ------------------ #
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        return jsonify({"message": "Invalid Email"}), 401

    if check_password_hash(user["password"], password):
        return (
            jsonify(
                {
                    "message": "Login Successful",
                    "user": {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                    },
                }
            ),
            200,
        )

    return jsonify({"message": "Invalid Password"}), 401
