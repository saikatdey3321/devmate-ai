
# import json
# import os
# import re

# from pathlib import Path
# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key) if api_key else None

# MEMORY_FILE = Path(__file__).with_name("memory.json")
# MAX_HISTORY_MESSAGES = 10
# conversation_history = []


# def load_memories():
#     """Load saved memories from memory.json."""
#     try:
#         with MEMORY_FILE.open("r", encoding="utf-8") as file:
#             data = json.load(file)

#         if isinstance(data, dict) and isinstance(data.get("memories"), list):
#             return data["memories"]

#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     return []


# def save_memories(memories):
#     """Save memories to memory.json."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump({"memories": memories}, file, indent=2)


# persistent_memories = load_memories()

# def add_memory(memory_type, value):
#     """Save a custom memory permanently."""
#     persistent_memories.append({
#         "type": memory_type,
#         "value": value
#     })

#     save_memories(persistent_memories)


# def extract_name(text):
#     """Extract a name from 'my name is ...'."""
#     match = re.search(r"\bmy name is\s+(.+)", text, re.IGNORECASE)

#     if not match:
#         return None

#     candidate = re.split(
#         r"[,.;!?]|\bthen\b|\bwhat is\b",
#         match.group(1),
#         maxsplit=1,
#         flags=re.IGNORECASE,
#     )[0].strip()

#     parts = candidate.split()[:2]
#     name = " ".join(parts).strip(" '-")

#     if re.fullmatch(
#         r"[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*)?",
#         name,
#     ):
#         return name

#     return None


# def remember(role, content):
#     """Keep the most recent conversation messages."""
#     conversation_history.append({"role": role, "content": content})

#     if len(conversation_history) > MAX_HISTORY_MESSAGES:
#         del conversation_history[:2]


# def find_remembered_name():
#     """Find the saved name in persistent memory."""
#     for memory in reversed(persistent_memories):
#         if memory.get("type") == "name":
#             return memory.get("value")

#     return None


# def ask_ai(question):
#     """Answer using the API or offline demo."""
#     if client is not None:
#         response = client.responses.create(
#             model="gpt-4.1-mini",
#             instructions=(
#                 "You are DevMate AI, a helpful programming tutor. "
#                 "Use the conversation history and saved memories below "
#                 "when relevant. Do not invent personal details.\n"
#                 f"Saved memories: {json.dumps(persistent_memories)}"
#             ),
#             input=conversation_history,
#         )
#         return response.output_text

#     question_lower = question.lower()

#     if "my name" in question_lower:
#         name = extract_name(question) or find_remembered_name()

#         if name:
#             return f"Your name is {name}."

#         return "You haven't told me your name yet."

#     if "hello" in question_lower or question_lower == "hi":
#         return "Hello! I'm DevMate AI. How can I help you?"

#     if "python" in question_lower:
#         return (
#             "Python is a programming language used in AI, "
#             "automation, and web development."
#         )

#     return (
#         "I'm running in offline demo mode. "
#         "I can remember your saved name across sessions."
#     )


# def main():
#     print("=" * 40)
#     print("Welcome to DevMate AI!")
#     print("Mode:", "AI" if client else "Offline demo")
#     print("Commands: help, memory, clear, exit")
#     print("=" * 40)

#     while True:
#         try:
#             question = input("\nYou: ").strip()
#         except (EOFError, KeyboardInterrupt):
#             print("\nDevMate AI: Goodbye! Keep learning.")
#             break

#         if not question:
#             print("DevMate AI: Please enter a question.")
#             continue

#         command = question.lower()

#         if command in ("exit", "quit"):
#             print("DevMate AI: Goodbye! Keep learning.")
#             break

#         if command == "help":
#             print(
#                 "Ask a question, type 'memory' to view saved memories, "
#                 "'clear' to reset session history, or 'exit' to quit."
#             )
#             continue

#                 if command.startswith("remember "):
#             fact = question[9:].strip()

#             if not fact:
#                 print("DevMate AI: Please tell me what to remember.")
#                 continue

#             add_memory("fact", fact)
#             print("DevMate AI: I'll remember that.")
#             continue

#         if command == "memory":
#             print("DevMate AI: Saved memories:", persistent_memories)
#             print(
#                 f"Session history: {len(conversation_history)} "
#                 f"of {MAX_HISTORY_MESSAGES} messages."
#             )
#             continue

#         if command == "clear":
#             conversation_history.clear()
#             print("DevMate AI: Session history cleared.")
#             continue

#         remember("user", question)

#         try:
#             name = extract_name(question)

#             if name:
#                 persistent_memories[:] = [
#                     memory
#                     for memory in persistent_memories
#                     if memory.get("type") != "name"
#                 ]
#                 persistent_memories.append({
#                     "type": "name",
#                     "value": name,
#                 })
#                 save_memories(persistent_memories)

#             answer = ask_ai(question)
#             remember("assistant", answer)
#             print("DevMate AI:", answer)

#         except Exception as error:
#             conversation_history.pop()
#             print(f"Request failed: {error}")


# if __name__ == "__main__":
#     main()





import json
import os
import re

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from router import detect_intent
from tools import save_memory, get_memories, forget_memory as forget_memory_tool


# -----------------------------
# Configuration
# -----------------------------

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

MEMORY_FILE = Path(__file__).with_name("memory.json")
MAX_HISTORY_MESSAGES = 10

conversation_history = []


# -----------------------------
# Persistent Memory
# -----------------------------

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
        json.dump(
            {"memories": memories},
            file,
            indent=2
        )


persistent_memories = load_memories()


def add_memory(memory_type, value):
    """Save a custom memory permanently."""
    persistent_memories.append({
        "type": memory_type,
        "value": value
    })

    save_memories(persistent_memories)

def forget_memory(keyword):
    """Remove saved memories containing the given keyword."""
    keyword = keyword.lower()

    removed_memories = []

    for memory in persistent_memories[:]:
        value = str(memory.get("value", ""))

        if keyword in value.lower():
            removed_memories.append(memory)
            persistent_memories.remove(memory)

    if removed_memories:
        save_memories(persistent_memories)

    return removed_memories


# -----------------------------
# Name Memory
# -----------------------------

def extract_name(text):
    """Extract a name from text such as 'My name is Saikat Dey'."""

    match = re.search(
        r"\bmy name is\s+(.+)",
        text,
        re.IGNORECASE
    )

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


def find_remembered_name():
    """Find the saved name from persistent memory."""

    for memory in reversed(persistent_memories):

        if memory.get("type") == "name":
            return memory.get("value")

    return None


def find_remembered_fact(keyword):
    """Find a saved fact containing the given keyword."""
    keyword = keyword.lower()

    for memory in reversed(persistent_memories):
        if memory.get("type") == "fact":
            value = memory.get("value", "")

            if keyword in value.lower():
                return value

    return None


# -----------------------------
# Conversation History
# -----------------------------

def remember(role, content):
    """Keep the most recent conversation messages."""

    conversation_history.append({
        "role": role,
        "content": content
    })

    if len(conversation_history) > MAX_HISTORY_MESSAGES:
        del conversation_history[:2]


# -----------------------------
# AI / Offline Response
# -----------------------------

def ask_ai(question):
    """Answer using OpenAI API or offline demo mode."""

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

    # -------------------------
    # Offline Demo Mode
    # -------------------------

    question_lower = question.lower()

    # Name-related questions
    if "my name" in question_lower:

        name = extract_name(question)

        if not name:
            name = find_remembered_name()

        if name:
            return f"Your name is {name}."

        return "You haven't told me your name yet."

    # Favorite language
    if "favorite language" in question_lower:

        fact = find_remembered_fact("favorite language")

        if fact:
            return f"You said: {fact}."

        return "I don't have your favorite language saved yet."

    # Greeting
    if "hello" in question_lower or question_lower == "hi":

        return "Hello! I'm DevMate AI. How can I help you?"

    # Python question
    if "python" in question_lower:

        return (
            "Python is a programming language used in AI, "
            "automation, and web development."
        )

    return (
        "I'm running in offline demo mode. "
        "I can remember your saved name and custom memories."
    )


# -----------------------------
# Main Application
# -----------------------------

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

        # Empty input
        if not question:

            print("DevMate AI: Please enter a question.")
            continue

        intent = detect_intent(question)
        print(f"[Router] Intent: {intent}")

        # -------------------------
        # Exit
        # -------------------------

        if intent == "exit":

            print("DevMate AI: Goodbye! Keep learning.")
            break

        # -------------------------
        # Help
        # -------------------------

        if intent == "help":

            print(
                "Ask a question, type 'memory' to view saved memories, "
                "use 'remember <fact>' to save a memory, "
                "'clear' to reset session history, "
                "or 'exit' to quit."
            )

            continue

        # -------------------------
        # Custom Remember Command
        # -------------------------

                # -------------------------
        # Custom Remember Command
        # -------------------------

        if intent == "remember":

            fact = question[9:].strip()

            if not fact:
                print(
                    "DevMate AI: Please tell me what to remember."
                )
                continue

            result = save_memory(
    "fact",
    fact,
    persistent_memories,
    save_memories
)

            print("DevMate AI: I'll remember that.")

            continue

        # -------------------------
        # Forget Memory Command
        # -------------------------

    
        if intent == "forget":

            keyword = question[7:].strip()

            if not keyword:
                print(
                    "DevMate AI: Please tell me what to forget."
                )
                continue

            removed_memories = forget_memory_tool(
                keyword,
                persistent_memories,
                save_memories
            )

            if removed_memories:
                print(
                    f"DevMate AI: Removed {len(removed_memories)} memory/memories."
                )
            else:
                print(
                    "DevMate AI: I couldn't find a matching memory."
                )

            continue


            if removed_memories:
                print(
                    f"DevMate AI: Removed {len(removed_memories)} memory."
                )
            else:
                print(
                    "DevMate AI: I couldn't find a matching memory."
                )

            continue

       

           
        # -------------------------
        # Memory Command
        # -------------------------

        
        if intent == "memory":

            saved = get_memories(persistent_memories)
            print("DevMate AI: Saved memories:", saved)

            print(
                f"Session history: "
                f"{len(conversation_history)} "
                f"of {MAX_HISTORY_MESSAGES} messages."
            )

            continue



                # -------------------------
        # Clear Persistent Memory
        # -------------------------

        if intent == "clear_memory":

            persistent_memories.clear()
            save_memories(persistent_memories)

            print(
                "DevMate AI: All persistent memories cleared."
            )

            continue

        # -------------------------
        # Clear Session History
        # -------------------------

        if intent == "clear":

            conversation_history.clear()

            print(
                "DevMate AI: Session history cleared."
            )

            continue

        # -------------------------
        # Normal Question
        # -------------------------

        remember("user", question)

        try:

            # Save name if user provides it
            name = extract_name(question)

            if name:

                # Remove previous saved name
                persistent_memories[:] = [
                    memory
                    for memory in persistent_memories
                    if memory.get("type") != "name"
                ]

                # Save latest name
                persistent_memories.append({
                    "type": "name",
                    "value": name,
                })

                save_memories(persistent_memories)

            # Generate response
            answer = ask_ai(question)

            remember("assistant", answer)

            print("DevMate AI:", answer)

        except Exception as error:

            # Remove failed user message
            conversation_history.pop()

            print(
                f"Request failed: {error}"
            )


# -----------------------------
# Application Entry Point
# -----------------------------

if __name__ == "__main__":
    main()