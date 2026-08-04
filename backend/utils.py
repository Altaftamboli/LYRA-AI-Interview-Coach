import re


# Validate Email
def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


# Validate Password
def validate_password(password):
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    return has_upper and has_lower and has_digit


# Calculate Score
def calculate_score(total_questions, correct_answers):
    if total_questions == 0:
        return 0

    return round((correct_answers / total_questions) * 100)


# Performance Level
def performance(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Needs Improvement"


# Create JSON Response
def response(message, status=True):
    return {"status": status, "message": message}
