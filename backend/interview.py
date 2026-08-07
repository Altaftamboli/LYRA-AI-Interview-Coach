from flask import Blueprint, request, jsonify
# from backend.ai.question_generator import generate_questions
from backend.ai.prompts import generate_question_prompt
from backend.ai.llm_client import ask_llm

interview_bp = Blueprint("interview", __name__, url_prefix="/api")


@interview_bp.route("/start-interview", methods=["POST"])
def start_interview():

    data = request.get_json()

    role = data.get("role")
    difficulty = data.get("difficulty")
    question_count =int(data.get("questions",1))

    # ai_questions = generate_questions(role, difficulty, question_count)
    ai_questions = []

    # for i in range(question_count):
    #     ai_questions.append(
    #         generate_question_prompt(role,difficulty)
    #     )
    #     question = Ask_llm(prompt)
    #     ai_questions.append(question)

    for i in range(question_count):
        prompt = generate_question_prompt(role,difficulty)
        question = ask_llm(prompt)
        ai_questions.append(question)
        

    return jsonify({"success": True, "questions": ai_questions})
