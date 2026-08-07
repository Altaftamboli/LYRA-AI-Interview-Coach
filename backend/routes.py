from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/login")
def login():
    return render_template("login.html")


@main_bp.route("/profile")
def profile():
    return render_template("profile.html")


@main_bp.route("/register")
def register():
    return render_template("register.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/interview")
def interview():
    return render_template("interview.html")


@main_bp.route("/result")
def result():
    return render_template("result.html")




