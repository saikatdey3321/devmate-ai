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

conversation_history = []


def ask_ai(question: str) -> str:
    """Answer using offline demo mode or the AI API."""

    if client is None:
        question_lower = question.lower()

        if "hello" in question_lower or question_lower == "hi":
            return "Hello! I'm DevMate AI. How can I help you?"

        if "python" in question_lower:
            return "Python is a programming language used in AI, automation, and web development."

        if "my name" in question_lower:
            for message in reversed(conversation_history):
                if message["role"] == "user" and "my name is" in message["content"].lower():
                    return "Your name is " + message["content"].split("is", 1)[1].strip().rstrip(".") + "."

            return "You haven't told me your name yet."

        return "I'm running in offline demo mode. I can remember messages in this session."

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="You are DevMate AI, a helpful programming tutor. Use the conversation history to answer follow-up questions.",
        input=conversation_history + [{"role": "user", "content": question}],
    )
    return response.output_text


def main():
    print("=" * 40)
    print("Welcome to DevMate AI!")
    print("Mode:", "AI" if client else "Offline demo")
    print("Type 'help' for help, 'clear' to reset memory, or 'exit' to quit.")
    print("=" * 40)

    while True:
        question = input("\nYou: ").strip()

        if not question:
            print("DevMate AI: Please enter a question.")
            continue

        command = question.lower()

        if command in ("exit", "quit"):
            print("DevMate AI: Goodbye! Keep learning.")
            break

        if command == "help":
            print("DevMate AI: Ask questions, use 'clear' to reset memory, or 'exit' to quit.")
            continue

        if command == "clear":
            conversation_history.clear()
            print("DevMate AI: Conversation memory cleared.")
            continue

        conversation_history.append({"role": "user", "content": question})

        try:
            answer = ask_ai(question)
            conversation_history.append({"role": "assistant", "content": answer})
            print("DevMate AI:", answer)
        except Exception as error:
            conversation_history.pop()
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
