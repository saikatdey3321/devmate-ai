
from app import ask_ai, remember, conversation_history


def get_response(question):
    """Get a response using DevMate AI's existing offline backend."""
    remember("user", question)

    answer = ask_ai(question)

    remember("assistant", answer)

    return answer
