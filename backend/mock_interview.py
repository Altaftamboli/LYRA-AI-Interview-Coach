from flask import Blueprint, render_template

mock_interview_bp = Blueprint("mock_interview", __name__)


@mock_interview_bp.route("/mock-interview")
def mock_interview():
    return render_template("mock_interview.html")
