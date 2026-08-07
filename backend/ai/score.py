import re


def calculate_score(evaluation):
    """
    Extracts the score from the AI evaluation.
    Returns an integer score out of 10.
    """

    try:
        match = re.search(r"Score\s*[:\-]?\s*(\d+)", evaluation, re.IGNORECASE)

        if match:
            return int(match.group(1))

        return 0

    except Exception:
        return 0