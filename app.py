
import json
import os
import re

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

MEMORY_FILE = Path(__file__).with_name("memory.json")
MAX_HISTORY_MESSAGES = 10
conversation_history = []


def load_memories():
    """Load saved memories from memory.json."""
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and isinstance(data.get("memories"), list):
            return data["memories"]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_memories(memories):
    """Save memories to memory.json."""
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump({"memories": memories}, file, indent=2)


persistent_memories = load_memories()


def extract_name(text):
    """Extract a name from 'my name is ...'."""
    match = re.search(r"\bmy name is\s+(.+)", text, re.IGNORECASE)

    if not match:
        return None

    candidate = re.split(
        r"[,.;!?]|\bthen\b|\bwhat is\b",
        match.group(1),
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()

    parts = candidate.split()[:2]
    name = " ".join(parts).strip(" '-")

    if re.fullmatch(
        r"[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*)?",
        name,
    ):
        return name

    return None


def remember(role, content):
    """Keep the most recent conversation messages."""
    conversation_history.append({"role": role, "content": content})

    if len(conversation_history) > MAX_HISTORY_MESSAGES:
        del conversation_history[:2]


def find_remembered_name():
    """Find the saved name in persistent memory."""
    for memory in reversed(persistent_memories):
        if memory.get("type") == "name":
            return memory.get("value")

    return None


def ask_ai(question):
    """Answer using the API or offline demo."""
    if client is not None:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are DevMate AI, a helpful programming tutor. "
                "Use the conversation history and saved memories below "
                "when relevant. Do not invent personal details.\n"
                f"Saved memories: {json.dumps(persistent_memories)}"
            ),
            input=conversation_history,
        )
        return response.output_text

    question_lower = question.lower()

    if "my name" in question_lower:
        name = extract_name(question) or find_remembered_name()

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
        "I can remember your saved name across sessions."
    )


def main():
    print("=" * 40)
    print("Welcome to DevMate AI!")
    print("Mode:", "AI" if client else "Offline demo")
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
                "Ask a question, type 'memory' to view saved memories, "
                "'clear' to reset session history, or 'exit' to quit."
            )
            continue

        if command == "memory":
            print("DevMate AI: Saved memories:", persistent_memories)
            print(
                f"Session history: {len(conversation_history)} "
                f"of {MAX_HISTORY_MESSAGES} messages."
            )
            continue

        if command == "clear":
            conversation_history.clear()
            print("DevMate AI: Session history cleared.")
            continue

        remember("user", question)

        try:
            name = extract_name(question)

            if name:
                persistent_memories[:] = [
                    memory
                    for memory in persistent_memories
                    if memory.get("type") != "name"
                ]
                persistent_memories.append({
                    "type": "name",
                    "value": name,
                })
                save_memories(persistent_memories)

            answer = ask_ai(question)
            remember("assistant", answer)
            print("DevMate AI:", answer)

        except Exception as error:
            conversation_history.pop()
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
