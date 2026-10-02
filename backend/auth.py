import os

from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from backend.database import get_db_connection

load_dotenv()

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

oauth = OAuth()

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# =========================================================
# REGISTER
# =========================================================


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required."}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters."}), 400

    conn = get_db_connection()

    if not conn:
        return jsonify({"message": "Database connection failed."}), 500

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        if cursor.fetchone():
            return jsonify({"message": "Email already registered."}), 409

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, password_hash, "user"),
        )

        conn.commit()

        return jsonify({"message": "Registration successful."}), 201

    except Exception as e:

        conn.rollback()

        print("Registration Error:", e)

        return jsonify({"message": "Registration failed."}), 500

    finally:

        cursor.close()
        conn.close()


# =========================================================
# NORMAL LOGIN
# =========================================================


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        session.clear()

        return jsonify({"message": "Email and password are required."}), 400

    conn = get_db_connection()

    if not conn:
        session.clear()

        return jsonify({"message": "Database connection failed."}), 500

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                role
            FROM users
            WHERE LOWER(email) = %s
            LIMIT 1
            """,
            (email,),
        )

        user = cursor.fetchone()

        # User doesn't exist
        if not user:

            session.clear()

            print("LOGIN FAILED - USER NOT FOUND:", email)

            return (
                jsonify({"success": False, "message": "Invalid email or password."}),
                401,
            )

        password_hash = user.get("password_hash")

        # Google-only account
        if not password_hash:

            session.clear()

            print("LOGIN FAILED - GOOGLE ACCOUNT:", email)

            return (
                jsonify(
                    {
                        "success": False,
                        "message": "This account uses Google Login. Please continue with Google.",
                    }
                ),
                401,
            )

        # =================================================
        # PASSWORD VERIFICATION
        # =================================================

        password_correct = check_password_hash(password_hash, password)

        print("LOGIN EMAIL:", email)
        print("PASSWORD CHECK:", password_correct)

        # WRONG PASSWORD
        if password_correct is not True:

            session.clear()

            print("LOGIN FAILED - WRONG PASSWORD:", email)

            return (
                jsonify({"success": False, "message": "Invalid email or password."}),
                401,
            )

        # =================================================
        # CORRECT PASSWORD
        # =================================================

        session.clear()

        session["user"] = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        }

        session.permanent = True

        print("LOGIN SUCCESS:", email)
        print("ROLE:", user["role"])

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Login successful.",
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

    except Exception as e:

        print("LOGIN ERROR:", e)

        session.clear()

        return jsonify({"success": False, "message": "Login failed."}), 500

    finally:

        cursor.close()
        conn.close()


# =========================================================
# LOGOUT
# =========================================================


@auth_bp.route("/logout", methods=["GET"])
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# GOOGLE LOGIN
# =========================================================


@auth_bp.route("/auth/google", methods=["GET"])
def google_login():

    try:

        redirect_uri = url_for("auth.google_callback", _external=True)

        print("GOOGLE REDIRECT URI:", redirect_uri)

        return google.authorize_redirect(redirect_uri, prompt="select_account")

    except Exception as e:

        print("Google Authorization Error:", e)

        return jsonify({"message": "Unable to start Google Login."}), 500


# =========================================================
# GOOGLE CALLBACK
# =========================================================


@auth_bp.route("/auth/google/callback", methods=["GET"])
def google_callback():

    try:

        token = google.authorize_access_token()

        user_info = token.get("userinfo")

        if not user_info:
            user_info = google.userinfo()

        if not user_info:
            return (
                jsonify({"message": "Unable to get Google account information."}),
                400,
            )

        email = user_info.get("email")
        name = user_info.get("name") or "Google User"

        if not email:
            return jsonify({"message": "Google account email not available."}), 400

        email = email.strip().lower()

        conn = get_db_connection()

        if not conn:
            return jsonify({"message": "Database connection failed."}), 500

        cursor = conn.cursor(dictionary=True)

        try:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    password_hash,
                    role
                FROM users
                WHERE email = %s
                LIMIT 1
                """,
                (email,),
            )

            user = cursor.fetchone()

            if not user:

                cursor.execute(
                    """
                    INSERT INTO users
                    (name, email, password_hash, role)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (name, email, None, "user"),
                )

                conn.commit()

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        email,
                        password_hash,
                        role
                    FROM users
                    WHERE email = %s
                    LIMIT 1
                    """,
                    (email,),
                )

                user = cursor.fetchone()

            else:

                cursor.execute(
                    """
                    UPDATE users
                    SET name = %s
                    WHERE id = %s
                    """,
                    (name, user["id"]),
                )

                conn.commit()

                user["name"] = name

            session.clear()

            session["user"] = {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
            }

            session.permanent = True

            print("GOOGLE LOGIN SUCCESS:", email)

            if user["role"] == "admin":
                return redirect("/admin/dashboard")

            return redirect("/dashboard")

        finally:

            cursor.close()
            conn.close()

    except Exception as e:

        print("GOOGLE LOGIN ERROR:", e)

        session.clear()

        return jsonify({"message": "Google login failed."}), 500
