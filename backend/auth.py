from flask import Blueprint, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import get_db_connection
from authlib.integrations.flask_client import OAuth
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

oauth = OAuth()

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))

        user = cursor.fetchone()

        if user:
            return jsonify({"message": "Email already exists"}), 400

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, hashed_password, "user"),
        )

        conn.commit()

        return jsonify({"message": "Registration Successful"}), 201

    except Exception as e:

        conn.rollback()

        print("Registration Error:", e)

        return jsonify({"message": "Registration failed"}), 500

    finally:

        cursor.close()
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT id, name, email, password_hash, role
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        user = cursor.fetchone()

    finally:

        cursor.close()
        conn.close()

    if user is None:
        return jsonify({"message": "Invalid Email"}), 401

    if not user["password_hash"]:
        return jsonify({"message": "This account uses Google Login"}), 401

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid Password"}), 401

    session["user"] = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }

    return (
        jsonify(
            {
                "message": "Login Successful",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                },
            }
        ),
        200,
    )


@auth_bp.route("/login/google")
def google_login():

    redirect_uri = url_for("auth.google_callback", _external=True)

    return google.authorize_redirect(redirect_uri, prompt="select_account")


@auth_bp.route("/auth/google/callback")
def google_callback():

    try:

        token = google.authorize_access_token()

        user_info = token.get("userinfo")

        if not user_info:
            user_info = google.userinfo()

        name = user_info.get("name", "")
        email = user_info.get("email", "")

        if not email:
            return "Google account email not available", 400

        conn = get_db_connection()

        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

        user = cursor.fetchone()

        if user:

            user_id = user["id"]
            role = user["role"]

            cursor.execute(
                """
                UPDATE users
                SET name = %s
                WHERE id = %s
                """,
                (name, user_id),
            )

        else:

            cursor.execute(
                """
                INSERT INTO users
                (name, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, None, "user"),
            )

            user_id = cursor.lastrowid
            role = "user"

        conn.commit()

        cursor.close()
        conn.close()

        session["user"] = {"id": user_id, "name": name, "email": email, "role": role}

        if role == "admin":
            return redirect("/admin/dashboard")

        return redirect("/dashboard")

    except Exception as e:

        print("Google Login Error:", e)

        return "Google Login Failed", 500
