from flask import Blueprint, request, jsonify, render_template, redirect, session
from werkzeug.security import check_password_hash
from backend.database import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET"])
def admin_login_page():
    return render_template("admin_login.html")


@admin_bp.route("/login", methods=["POST"])
def admin_login():

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
        return jsonify({"message": "Invalid admin credentials"}), 401

    if user["role"] != "admin":
        return jsonify({"message": "Access denied. Admin account required."}), 403

    if not user["password_hash"]:
        return jsonify({"message": "Admin must use password login"}), 401

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid admin credentials"}), 401

    session["admin"] = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }

    return (
        jsonify({"message": "Admin login successful", "redirect": "/admin/dashboard"}),
        200,
    )


@admin_bp.route("/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    conn = get_db_connection()

    if conn is None:
        return "Database connection failed", 500

    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()["total_users"]

        cursor.execute("SELECT COUNT(*) AS total_interviews FROM interviews")
        total_interviews = cursor.fetchone()["total_interviews"]

        cursor.execute("""
            SELECT COUNT(*) AS total_admins
            FROM users
            WHERE role = 'admin'
            """)
        total_admins = cursor.fetchone()["total_admins"]

    finally:

        cursor.close()
        conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_interviews=total_interviews,
        total_admins=total_admins,
    )


@admin_bp.route("/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin/login")
