from flask import Blueprint, request, jsonify
from backend.database import get_db_connection

interview_bp = Blueprint("interview", __name__)


# Save Interview Answer
@interview_bp.route("/submit-answer", methods=["POST"])
def submit_answer():
    data = request.get_json()

    user_id = data.get("user_id")
    question = data.get("question")
    answer = data.get("answer")

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO interview_answers(user_id, question, answer)
    VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (user_id, question, answer))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Answer submitted successfully"}), 201


# Get All Answers of a User
@interview_bp.route("/answers/<int:user_id>", methods=["GET"])
def get_answers(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM interview_answers WHERE user_id=%s", (user_id,))

    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(answers), 200
