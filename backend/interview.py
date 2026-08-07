from flask import Blueprint, request, jsonify
# from backend.ai.question_generator import generate_questions
from backend.ai.prompts import generate_question_prompt

interview_bp = Blueprint("interview", __name__, url_prefix="/api")


@interview_bp.route("/start-interview", methods=["POST"])
def start_interview():

    data = request.get_json()

    role = data.get("role")
    difficulty = data.get("difficulty")
    question_count = data.get("questions")

    ai_questions = generate_questions(role, difficulty, question_count)

    return jsonify({"success": True, "questions": ai_questions})
