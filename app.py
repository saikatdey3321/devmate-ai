
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

conversation_history = []
MAX_HISTORY_MESSAGES = 10


def extract_name(text: str) -> str | None:
    """Extract a name from a statement such as 'My name is Saikat Dey'."""
    match = re.search(r"\bmy name is\s+(.+)", text, re.IGNORECASE)

    if not match:
        return None

    # Stop at punctuation or a follow-up phrase.
    candidate = re.split(
        r"[,.;!?]|\bthen\b|\band\s+what\b|\bwhat\s+is\b",
        match.group(1),
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()

    # Keep at most two name parts for this beginner demo.
    parts = candidate.split()[:2]
    name = " ".join(parts).strip(" '-")

    if not name or not re.fullmatch(r"[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*)?", name):
        return None

    return name


def remember(role: str, content: str) -> None:
    """Store messages while keeping complete user-assistant pairs."""
    conversation_history.append({
        "role": role,
        "content": content,
    })

    if len(conversation_history) > MAX_HISTORY_MESSAGES:
        # Remove complete old pairs, not individual messages.
        del conversation_history[:2]


def find_remembered_name() -> str | None:
    """Find the most recent name statement in earlier user messages."""
    for message in reversed(conversation_history[:-1]):
        if message["role"] == "user":
            name = extract_name(message["content"])

            if name:
                return name

    return None


def ask_ai(question: str) -> str:
    """Answer using offline demo rules or the OpenAI API."""

    if client is not None:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are DevMate AI, a helpful programming tutor. "
                "Use the recent conversation history to answer follow-up "
                "questions. Do not claim to remember information that is "
                "not present in the supplied history."
            ),
            input=conversation_history,
        )
        return response.output_text

    question_lower = question.lower()

    # Support a name statement and question in the same input.
    if "my name" in question_lower:
        name = extract_name(question)

        if name:
            return f"Your name is {name}."

        name = find_remembered_name()

        if name:
            return f"Your name is {name}."

        return "You haven't told me your name yet."

    if "hello" in question_lower or question_lower == "hi":
        return "Hello! I'm DevMate AI. How can I help you?"

    if "python" in question_lower:
        return (
            "Python is a programming language used in AI, "
            "automation, and web development."
        )

    return (
        "I'm running in offline demo mode. "
        "I can recognize names and remember recent messages in this session."
    )


def main() -> None:
    print("=" * 40)
    print("Welcome to DevMate AI!")
    print("Mode:", "AI" if client else "Offline demo")
    print("Memory limit:", MAX_HISTORY_MESSAGES, "messages")
    print("Commands: help, memory, clear, exit")
    print("=" * 40)

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDevMate AI: Goodbye! Keep learning.")
            break

        if not question:
            print("DevMate AI: Please enter a question.")
            continue

        command = question.lower()

        if command in ("exit", "quit"):
            print("DevMate AI: Goodbye! Keep learning.")
            break

        if command == "help":
            print(
                "DevMate AI: Ask a question, type 'memory' to inspect "
                "memory, 'clear' to reset it, or 'exit' to quit."
            )
            continue

        if command == "memory":
            print(
                f"DevMate AI: Stored {len(conversation_history)} "
                f"of {MAX_HISTORY_MESSAGES} allowed messages."
            )
            continue

        if command == "clear":
            conversation_history.clear()
            print("DevMate AI: Conversation memory cleared.")
            continue

        remember("user", question)

        try:
            answer = ask_ai(question)
            remember("assistant", answer)
            print("DevMate AI:", answer)

        except Exception as error:
            # Remove the failed user message.
            conversation_history.pop()
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
