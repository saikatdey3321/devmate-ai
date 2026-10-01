import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key missing. Check your .env file.")

client = OpenAI(api_key=api_key)


def ask_ai(question: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="You are DevMate AI, a helpful programming tutor.",
        input=question,
    )
    return response.output_text


def main():
    print("Welcome to DevMate AI!")
    question = input("Ask your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    try:
        print("\nDevMate AI:", ask_ai(question))
    except Exception as error:
        print(f"Request failed: {error}")


if __name__ == "__main__":
    main()