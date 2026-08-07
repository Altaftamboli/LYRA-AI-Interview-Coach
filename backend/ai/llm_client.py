from groq import Groq

from backend.ai.config import GROQ_API_KEY, MODEL_NAME


# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to the Groq LLM and returns the response.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content.strip()
        print(result)
        return result

    except Exception as e:
        return f"Error: {str(e)}"