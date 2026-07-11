from flask import Blueprint, jsonify
from backend.database import get_db_connection

report_bp = Blueprint("report", __name__)


@report_bp.route("/report/<int:user_id>", methods=["GET"])
def generate_report(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT question, answer FROM interview_answers WHERE user_id=%s", (user_id,)
    )

    answers = cursor.fetchall()

    total_questions = len(answers)

    if total_questions == 0:
        return jsonify({"message": "No interview found."}), 404

    score = total_questions * 10

    report = {
        "user_id": user_id,
        "questions_answered": total_questions,
        "score": score,
        "status": "Completed",
        "answers": answers,
    }

    cursor.close()
    conn.close()

    return jsonify(report), 200
