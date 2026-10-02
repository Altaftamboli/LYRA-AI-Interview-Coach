from flask import Blueprint, render_template, session, redirect

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/login")
def login_page():
    return render_template("login.html")


@main_bp.route("/register")
def register_page():
    return render_template("register.html")


@main_bp.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@main_bp.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html")


@main_bp.route("/interview")
def interview():

    if "user" not in session:
        return redirect("/login")

    return render_template("interview.html")


@main_bp.route("/result")
def result():

    if "user" not in session:
        return redirect("/login")

    return render_template("result.html")
