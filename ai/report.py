from ai.score import calculate_score


def generate_report(question, answer, evaluation):
    """
    Generates the final interview report.
    """

    score = calculate_score(evaluation)

    report = {
        "Question": question,
        "Answer": answer,
        "Score": f"{score}/10",
        "Evaluation": evaluation
    }

    return report