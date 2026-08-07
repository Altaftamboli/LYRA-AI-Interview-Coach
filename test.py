from ai.llm_client import ask_llm
from ai.prompts import generate_question_prompt, evaluate_answer_prompt
import re


def extract_score(text):
    match = re.search(r'(\d+(\.\d+)?)\s*/\s*10', text)
    if match:
        return float(match.group(1))
    return 0


def main():
    print("=" * 60)
    print("            LYRA AI Interview Coach")
    print("=" * 60)

    role = input("Enter Job Role: ")
    difficulty = input("Difficulty (Easy/Medium/Hard): ")

    print("\nHow many questions?")
    print("1. 5 Questions")
    print("2. 10 Questions")
    print("3. 15 Questions")

    choice = input("Choose (1/2/3): ")

    if choice == "1":
        total_questions = 5
    elif choice == "2":
        total_questions = 10
    elif choice == "3":
        total_questions = 15
    else:
        total_questions = 5

    scores = []

    for i in range(total_questions):

        print("\n" + "=" * 60)
        print(f"Question {i+1}/{total_questions}")
        print("=" * 60)

        prompt = generate_question_prompt(role, difficulty)
        question = ask_llm(prompt)

        print("\nInterview Question:\n")
        print(question)

        answer = input("\nYour Answer:\n> ")

        print("\nEvaluating...\n")

        eval_prompt = evaluate_answer_prompt(question, answer)
        evaluation = ask_llm(eval_prompt)

        print(evaluation)

        score = extract_score(evaluation)
        scores.append(score)

        if i != total_questions - 1: 
            input("\nPress Enter for Next Question...")

    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)

    total = 0

    for i, score in enumerate(scores):
        print(f"Question {i+1}: {score}/10")
        total += score

    average = total / len(scores)

    print("\nAverage Score: {:.2f}/10".format(average))

    if average >= 9:
        verdict = "Excellent"
    elif average >= 8:
        verdict = "Very Good"
    elif average >= 7:
        verdict = "Good"
    elif average >= 6:
        verdict = "Average"
    else:
        verdict = "Needs Improvement"

    print("Verdict:", verdict)

    print("\nThank you for attending the interview!")


if __name__ == "__main__":
    main()