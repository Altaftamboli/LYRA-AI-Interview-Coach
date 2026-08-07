from ai.llm_client import ask_llm
from ai.prompts import evaluate_answer_prompt


def evaluate_answer(question, answer):
    """
    Evaluates a candidate's answer using the LLM.
    """

    try:
        prompt = evaluate_answer_prompt(question, answer)
        response = ask_llm(prompt)

        return response

    except Exception as e:
        return f"Evaluation Error: {str(e)}"