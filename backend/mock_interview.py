from flask import Blueprint, request, jsonify, render_template
from backend.ai.llm_client import ask_llm

import json
import re


mock_interview_bp = Blueprint(
    "mock_interview",
    __name__
)


# ==========================================
# MOCK INTERVIEW PAGE
# ==========================================

@mock_interview_bp.route("/mock-interview")
def mock_interview():

    return render_template(
        "mock_interview.html"
    )


# ==========================================
# START MOCK INTERVIEW
# ==========================================

@mock_interview_bp.route(
    "/api/mock-interview/start",
    methods=["POST"]
)
def start_mock_interview():

    data = request.get_json(
        silent=True
    ) or {}


    role = data.get(
        "role",
        "Software Developer"
    )


    difficulty = data.get(
        "difficulty",
        "Medium"
    )


    try:

        question_count = int(
            data.get(
                "questions",
                5
            )
        )

    except (TypeError, ValueError):

        question_count = 5


    question_count = max(
        1,
        min(
            question_count,
            15
        )
    )


    prompt = f"""
You are LYRA, an expert AI technical interviewer.

Create a mock interview for:

Job Role: {role}
Difficulty: {difficulty}
Number of Questions: {question_count}

Generate exactly {question_count} unique interview questions.

Include:

- Technical knowledge
- Practical problem solving
- Real-world situations
- Role-specific concepts
- Conceptual understanding

Return ONLY valid JSON:

{{
    "questions": [
        "Question 1",
        "Question 2"
    ]
}}

Rules:

- Generate exactly {question_count} questions.
- Every question must be unique.
- Do not provide answers.
- Do not provide explanations.
- Do not use Markdown.
"""


    try:

        response = ask_llm(
            prompt
        )


        if not response:

            return jsonify({
                "success": False,
                "message":
                    "AI returned no questions."
            }), 500


        result = parse_json_response(
            response
        )


        questions = result.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            raise ValueError(
                "Invalid question format."
            )


        cleaned_questions = []


        for question in questions:

            if not isinstance(
                question,
                str
            ):

                continue


            question =question.strip()


            if (
                question
                and
                question not in cleaned_questions
            ):

                cleaned_questions.append(
                    question
                )


        if not cleaned_questions:

            return jsonify({
                "success": False,
                "message":
                    "AI did not generate valid questions."
            }), 500


        return jsonify({

            "success": True,

            "questions":
                cleaned_questions[
                    :question_count
                ]

        }), 200


    except Exception as e:

        print(
            "START MOCK INTERVIEW ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                "Failed to generate mock interview questions."

        }), 500


# ==========================================
# EVALUATE ANSWER
# ==========================================

@mock_interview_bp.route(
    "/api/mock-interview/evaluate-answer",
    methods=["POST"]
)
def evaluate_answer():

    data = request.get_json(
        silent=True
    ) or {}


    role = data.get(
        "role",
        "Software Developer"
    )


    difficulty = data.get(
        "difficulty",
        "Medium"
    )


    question = data.get(
        "question",
        ""
    )


    answer = data.get(
        "answer",
        ""
    )


    if not question or not answer:

        return jsonify({

            "success": False,

            "message":
                "Question and answer are required."

        }), 400


    prompt = f"""
You are LYRA, an expert technical interviewer.

Evaluate the candidate's answer.

Job Role:
{role}

Difficulty:
{difficulty}

Question:
{question}

Candidate Answer:
{answer}

Evaluate:

- Technical correctness
- Relevance
- Completeness
- Clarity
- Understanding

Return ONLY valid JSON:

{{
    "score": 0,
    "technical_correctness": 0,
    "relevance": 0,
    "completeness": 0,
    "clarity": 0,
    "feedback": "",
    "improvement": ""
}}

Rules:

- All scores must be integers from 0 to 100.
- Give useful feedback.
- Give practical improvement advice.
- Do not use Markdown.
- Do not add text outside JSON.
"""


    try:

        response = ask_llm(
            prompt
        )


        if not response:

            return jsonify({

                "success": False,

                "message":
                    "AI returned no evaluation."

            }), 500


        evaluation =parse_json_response(
                response
            )


        evaluation =normalize_evaluation(
                evaluation
            )


        return jsonify({

            "success": True,

            "evaluation":
                evaluation

        }), 200


    except Exception as e:

        print(
            "ANSWER EVALUATION ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                "Failed to analyze the answer."

        }), 500


# ==========================================
# FINAL REPORT
# ==========================================

@mock_interview_bp.route(
    "/api/mock-interview/final-report",
    methods=["POST"]
)
def final_report():

    data = request.get_json(
        silent=True
    ) or {}


    role = data.get(
        "role",
        "Software Developer"
    )


    difficulty = data.get(
        "difficulty",
        "Medium"
    )


    questions = data.get(
        "questions",
        []
    )


    answers = data.get(
        "answers",
        []
    )


    evaluations = data.get(
        "evaluations",
        []
    )


    if not questions:

        return jsonify({

            "success": False,

            "message":
                "No interview questions found."

        }), 400


    interview_data = []


    for index, question in enumerate(
        questions
    ):

        answer_data = (
            answers[index]
            if index < len(answers)
            else {}
        )


        evaluation = (
            evaluations[index]
            if index < len(evaluations)
            else {}
        )


        interview_data.append({

            "question":
                question,

            "answer":
                answer_data.get(
                    "answer",
                    ""
                ),

            "evaluation":
                evaluation

        })


    interview_json = json.dumps(
        interview_data,
        ensure_ascii=False,
        indent=2
    )


    prompt = f"""
You are LYRA, an expert interview coach.

Generate the final performance report.

Job Role:
{role}

Difficulty:
{difficulty}

Interview Data:

{interview_json}

Return ONLY valid JSON:

{{
    "score": 0,
    "strengths": [],
    "weaknesses": [],
    "suggestions": []
}}

Rules:

- Score must be between 0 and 100.
- Strengths must contain exactly 3 points.
- Weaknesses must contain exactly 3 points.
- Suggestions must contain exactly 3 practical points.
- Consider the complete interview.
- Do not use Markdown.
- Do not add text outside JSON.
"""


    try:

        response = ask_llm(
            prompt
        )


        if not response:

            return jsonify({

                "success": False,

                "message":
                    "AI returned no final report."

            }), 500


        report =parse_json_response(
                response
            )


        report =normalize_report(
                report
            )


        return jsonify({

            "success": True,

            "report":
                report

        }), 200


    except Exception as e:

        print(
            "FINAL REPORT ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "message":
                "Failed to generate final report."

        }), 500


# ==========================================
# JSON PARSER
# ==========================================

def parse_json_response(
    response
):

    cleaned = response.strip()


    cleaned =re.sub(r"```json", "",cleaned,
            flags=re.IGNORECASE)


    cleaned = re.sub(r"```","",cleaned)


    cleaned = cleaned.strip()


    start = cleaned.find("{")

    end = cleaned.rfind("}")


    if (
        start == -1
        or end == -1
    ):

        raise ValueError(
            "AI response does not contain valid JSON."
        )


    cleaned =cleaned[
            start:end + 1
        ]


    return json.loads(
        cleaned
    )


# ==========================================
# NORMALIZE EVALUATION
# ==========================================

def normalize_evaluation(
    evaluation
):

    return {

        "score":
            safe_score(
                evaluation.get(
                    "score",
                    0
                )
            ),

        "technical_correctness":
            safe_score(
                evaluation.get(
                    "technical_correctness",
                    0
                )
            ),

        "relevance":
            safe_score(
                evaluation.get(
                    "relevance",
                    0
                )
            ),

        "completeness":
            safe_score(
                evaluation.get(
                    "completeness",
                    0
                )
            ),

        "clarity":
            safe_score(
                evaluation.get(
                    "clarity",
                    0
                )
            ),

        "feedback":
            str(
                evaluation.get(
                    "feedback",
                    ""
                )
            ),

        "improvement":
            str(
                evaluation.get(
                    "improvement",
                    ""
                )
            )

    }


# ==========================================
# NORMALIZE REPORT
# ==========================================

def normalize_report(
    report
):

    return {

        "score":
            safe_score(
                report.get(
                    "score",
                    0
                )
            ),

        "strengths":
            clean_list(
                report.get(
                    "strengths",
                    []
                )
            )[:3],

        "weaknesses":
            clean_list(
                report.get(
                    "weaknesses",
                    []
                )
            )[:3],

        "suggestions":
            clean_list(
                report.get(
                    "suggestions",
                    []
                )
            )[:3]

    }


# ==========================================
# SAFE SCORE
# ==========================================

def safe_score(
    value
):

    try:

        value =int(float(value)
            )

    except (
        TypeError,
        ValueError
    ):

        value = 0


    return max(
        0,
        min(
            value,
            100
        )
    )


# ==========================================
# CLEAN LIST
# ==========================================

def clean_list(
    value
):

    if not isinstance(
        value,
        list
    ):

        return []


    result = []


    for item in value:

        if isinstance(
            item,
            str
        ):

            item = item.strip()


            if item:

                result.append(
                    item
                )


    return result