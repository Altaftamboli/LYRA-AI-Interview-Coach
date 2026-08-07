def generate_question_prompt(role, difficulty, previous_questions=""):
    """
    Generates interview questions based on role and difficulty.
    """

    return f"""
You are a professional AI Interviewer.

Generate ONE interview question.

Role: {role}
Difficulty: {difficulty}

Rules:
- Ask only one question.
- Do not provide the answer.
- Keep the question clear and professional.
- Return only the interview question.
"""


def evaluate_answer_prompt(question, answer):
    """
    Evaluates the candidate's answer.
    """

    return f"""
You are an AI Interview Evaluator.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer based on:
1. Technical Accuracy
2. Clarity
3. Communication
4. Confidence

Provide:
- Score out of 10
- Strengths
- Weaknesses
- Suggestions for improvement

Keep the response professional and concise.
"""