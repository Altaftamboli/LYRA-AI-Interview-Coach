from backend.ai.ai_service import generate


def generate_questions(role, difficulty, question_count):

    prompt = f"""
You are LYRA AI Interview Coach.

Generate {question_count} interview questions.

Job Role:
{role}

Difficulty:
{difficulty}

Rules:

1. Ask interview questions only.
2. Do not provide answers.
3. Number each question.
4. Keep questions relevant to the selected role.
"""

    return generate(prompt)
