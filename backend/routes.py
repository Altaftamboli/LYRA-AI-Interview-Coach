from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return jsonify({"message": "AI Interview Coach Backend Running"})


@main_bp.route("/dashboard")
def dashboard():
    return jsonify({"message": "Dashboard Loaded"})


@main_bp.route("/health")
def health():
    return jsonify({"status": "OK"})
