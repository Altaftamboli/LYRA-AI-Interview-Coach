from flask import Blueprint, request, jsonify
from backend.ai.prompts import generate_question_prompt
from backend.ai.llm_client import ask_llm
import json
import re

interview_bp = Blueprint(
    "interview",
    __name__,
    url_prefix="/api"
)


@interview_bp.route("/start-interview", methods=["POST"])
def start_interview():

    data = request.get_json() or {}

    role = data.get("role")
    difficulty = data.get("difficulty")
    question_count = int(data.get("questions", 1))

    if not role or not difficulty:
        return jsonify({
            "success": False,
            "message": "Role and difficulty are required."
        }), 400

    ai_questions = []

    for i in range(question_count):

        prompt = generate_question_prompt(
            role,
            difficulty
        )

        prompt += f"""

This is interview question {i + 1}.

Generate ONE unique interview question.

Do not repeat questions from common examples.
Do not generate multiple questions.
Return only the question text.
"""

        question = ask_llm(prompt)

        if question:

            question = question.strip()

            if question not in ai_questions:
                ai_questions.append(question)

    if not ai_questions:

        return jsonify({
            "success": False,
            "message": "AI could not generate questions."
        }), 500

    return jsonify({
        "success": True,
        "questions": ai_questions
    }), 200


@interview_bp.route("/evaluate-interview", methods=["POST"])
def evaluate_interview():

    data = request.get_json() or {}

    questions = data.get("questions", [])
    answers = data.get("answers", [])

    role = data.get(
        "role",
        "Software Developer"
    )

    difficulty = data.get(
        "difficulty",
        "Medium"
    )


    if not questions or not answers:

        return jsonify({
            "success": False,
            "message": "Questions and answers are required."
        }), 400


    qa_text = ""

    for i, question in enumerate(questions):

        answer = ""

        if i < len(answers):
            answer = answers[i]

        qa_text += f"""
Question {i + 1}:
{question}

Candidate Answer:
{answer}

"""


    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's interview performance.

Job Role: {role}
Difficulty: {difficulty}

Interview:

{qa_text}

Evaluate every answer using:

- Technical correctness
- Relevance
- Completeness
- Understanding
- Clarity

Return ONLY valid JSON.

Use exactly this structure:

{{
    "score": 0,
    "totalQuestions": {len(questions)},
    "correctAnswers": 0,
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "feedback": []
}}

Rules:

1. score must be an integer between 0 and 100.
2. totalQuestions must be {len(questions)}.
3. correctAnswers must contain the number of substantially correct answers.
4. strengths must contain 3 points.
5. weaknesses must contain 3 points.
6. suggestions must contain 3 useful suggestions.
7. feedback must contain exactly one feedback item for every question.
8. Do not use Markdown.
9. Do not add text before or after the JSON.
"""


    try:

        response = ask_llm(prompt)

        if not response:

            return jsonify({
                "success": False,
                "message": "AI evaluation returned no response."
            }), 500


        cleaned_response = response.strip()


        cleaned_response = re.sub(
            r"```json",
            "",
            cleaned_response,
            flags=re.IGNORECASE
        )

        cleaned_response = re.sub(
            r"```",
            "",
            cleaned_response
        )

        cleaned_response = cleaned_response.strip()


        start = cleaned_response.find("{")
        end = cleaned_response.rfind("}")


        if start != -1 and end != -1:

            cleaned_response = cleaned_response[start:end + 1]


        result = json.loads(
            cleaned_response
        )


        result["success"] = True


        return jsonify(
            result
        ), 200


    except json.JSONDecodeError as e:

        print(
            "JSON Evaluation Error:",
            e
        )

        print(
            "AI Response:",
            response
        )

        return jsonify({
            "success": False,
            "message":
                "AI returned an invalid evaluation.",
            "raw_response": response
        }), 500


    except Exception as e:

        print(
            "Interview Evaluation Error:",
            e
        )

        return jsonify({
            "success": False,
            "message":
                "Failed to evaluate interview."
        }), 500