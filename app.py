# import os
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")

# if not api_key:
#     raise ValueError("API key missing. Check your .env file.")

# client = OpenAI(api_key=api_key)


# def ask_ai(question: str) -> str:
#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         instructions="You are DevMate AI, a helpful programming tutor.",
#         input=question,
#     )
#     return response.output_text


# def main():
#     print("Welcome to DevMate AI!")
#     question = input("Ask your question: ").strip()

#     if not question:
#         print("Please enter a question.")
#         return

#     try:
#         print("\nDevMate AI:", ask_ai(question))
#     except Exception as error:
#         print(f"Request failed: {error}")


# if __name__ == "__main__":
#     main()






import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None


def ask_ai(question: str) -> str:
    """Answer a question using AI or offline demo mode."""

    if client is None:
        question_lower = question.lower()

        if "hello" in question_lower or "hi" == question_lower:
            return "Hello! I'm DevMate AI. How can I help you?"

        if "python" in question_lower:
            return "Python is a programming language used in AI, automation, and web development."

        if "help" in question_lower:
            return "Ask me about Python, or type 'exit' to quit."

        return (
            "I'm running in offline demo mode. "
            "AI answers will be enabled when we configure the API key."
        )

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="You are DevMate AI, a helpful programming tutor.",
        input=question,
    )
    return response.output_text


def main():
    print("=" * 40)
    print("Welcome to DevMate AI!")
    print("Mode:", "AI" if client else "Offline demo")
    print("Type 'help' for help or 'exit' to quit.")
    print("=" * 40)

    while True:
        question = input("\nYou: ").strip()

        if not question:
            print("DevMate AI: Please enter a question.")
            continue

        if question.lower() in ("exit", "quit"):
            print("DevMate AI: Goodbye! Keep learning.")
            break

        if question.lower() == "help":
            print("DevMate AI:", ask_ai("help"))
            continue

        try:
            print("DevMate AI:", ask_ai(question))
        except Exception as error:
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
