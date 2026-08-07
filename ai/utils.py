import json


def clean_text(text):
    """
    Removes extra spaces and newlines.
    """
    if not text:
        return ""

    return " ".join(text.strip().split())


def format_response(response):
    """
    Formats the LLM response.
    """
    return clean_text(response)


def save_report(report, filename="interview_report.json"):
    """
    Saves the interview report as a JSON file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return True

    except Exception:
        return False