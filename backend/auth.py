from flask import Blueprint, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import get_db_connection
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

# ---------------- Google OAuth ---------------- #
oauth = OAuth()

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# ---------------- Register ---------------- #
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
        "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
        (name, email, hashed_password),
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Registration Successful"}), 201


# ---------------- Login ---------------- #
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


# ---------------- Google Login ---------------- #
@auth_bp.route("/login/google")
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


# ---------------- Google Callback ---------------- #
@auth_bp.route("/auth/google/callback")
def google_callback():

    token = google.authorize_access_token()
    user = token["userinfo"]

    session["user"] = {"name": user["name"], "email": user["email"]}

    return redirect("/dashboard")
