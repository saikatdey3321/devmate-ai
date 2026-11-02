
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





# import json
# import os
# import re

# from pathlib import Path
# from dotenv import load_dotenv
# from openai import OpenAI
# from router import detect_intent
# from tools import save_memory, get_memories, forget_memory as forget_memory_tool


# # -----------------------------
# # Configuration
# # -----------------------------

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key) if api_key else None

# MEMORY_FILE = Path(__file__).with_name("memory.json")
# MAX_HISTORY_MESSAGES = 10

# conversation_history = []


# # -----------------------------
# # Persistent Memory
# # -----------------------------

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
#         json.dump(
#             {"memories": memories},
#             file,
#             indent=2
#         )


# persistent_memories = load_memories()


# def add_memory(memory_type, value):
#     """Save a custom memory permanently."""
#     persistent_memories.append({
#         "type": memory_type,
#         "value": value
#     })

#     save_memories(persistent_memories)

# def forget_memory(keyword):
#     """Remove saved memories containing the given keyword."""
#     keyword = keyword.lower()

#     removed_memories = []

#     for memory in persistent_memories[:]:
#         value = str(memory.get("value", ""))

#         if keyword in value.lower():
#             removed_memories.append(memory)
#             persistent_memories.remove(memory)

#     if removed_memories:
#         save_memories(persistent_memories)

#     return removed_memories


# # -----------------------------
# # Name Memory
# # -----------------------------

# def extract_name(text):
#     """Extract a name from text such as 'My name is Saikat Dey'."""

#     match = re.search(
#         r"\bmy name is\s+(.+)",
#         text,
#         re.IGNORECASE
#     )

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


# def find_remembered_name():
#     """Find the saved name from persistent memory."""

#     for memory in reversed(persistent_memories):

#         if memory.get("type") == "name":
#             return memory.get("value")

#     return None


# def find_remembered_fact(keyword):
#     """Find a saved fact containing the given keyword."""
#     keyword = keyword.lower()

#     for memory in reversed(persistent_memories):
#         if memory.get("type") == "fact":
#             value = memory.get("value", "")

#             if keyword in value.lower():
#                 return value

#     return None


# # -----------------------------
# # Conversation History
# # -----------------------------

# def remember(role, content):
#     """Keep the most recent conversation messages."""

#     conversation_history.append({
#         "role": role,
#         "content": content
#     })

#     if len(conversation_history) > MAX_HISTORY_MESSAGES:
#         del conversation_history[:2]


# # -----------------------------
# # AI / Offline Response
# # -----------------------------

# # def ask_ai(question):
# #     """Answer using OpenAI API or offline demo mode."""

# #     if client is not None:

# #         response = client.responses.create(
# #             model="gpt-4.1-mini",
# #             instructions=(
# #                 "You are DevMate AI, a helpful programming tutor. "
# #                 "Use the conversation history and saved memories below "
# #                 "when relevant. Do not invent personal details.\n"
# #                 f"Saved memories: {json.dumps(persistent_memories)}"
# #             ),
# #             input=conversation_history,
# #         )

# #         return response.output_text

# #     # -------------------------
# #     # Offline Demo Mode
# #     # -------------------------

# #     question_lower = question.lower()

# #     # Name-related questions
# #     if "my name" in question_lower:

# #         name = extract_name(question)

# #         if not name:
# #             name = find_remembered_name()

# #         if name:
# #             return f"Your name is {name}."

# #         return "You haven't told me your name yet."

# #     # Favorite language
# #     if "favorite language" in question_lower:

# #         fact = find_remembered_fact("favorite language")

# #         if fact:
# #             return f"You said: {fact}."

# #         return "I don't have your favorite language saved yet."

# #     # Greeting
# #     if "hello" in question_lower or question_lower == "hi":

# #         return "Hello! I'm DevMate AI. How can I help you?"

# #     # Python question
# #     if "python" in question_lower:

# #         return (
# #             "Python is a programming language used in AI, "
# #             "automation, and web development."
# #         )

# #     return (
# #         "I'm running in offline demo mode. "
# #         "I can remember your saved name and custom memories."
# #     )


# def ask_ai(question):
#     """Answer using OpenAI API or memory-aware offline demo mode."""

#     if client is not None:

#         response = client.responses.create(
#             model="gpt-4.1-mini",
#             instructions=(
#                 "You are DevMate AI, a helpful programming tutor. "
#                 "Use conversation history and saved memories when relevant. "
#                 "Do not invent personal information.\n"
#                 f"Saved memories: {json.dumps(persistent_memories)}"
#             ),
#             input=conversation_history,
#         )

#         return response.output_text

#     # -------------------------
#     # Offline Demo Mode
#     # -------------------------

#     question_lower = question.lower()

#     # 1. Name-related questions
#     if "my name" in question_lower:

#         name = extract_name(question)

#         if not name:
#             name = find_remembered_name()

#         if name:
#             return f"Your name is {name}."

#         return "You haven't told me your name yet."

#     # 2. Questions about learning and goals
#     if any(word in question_lower for word in [
#         "learning", "learn", "study", "studying"
#     ]):

#         learning_memories = [
#             item.get("value", "")
#             for item in persistent_memories
#             if any(
#                 word in item.get("value", "").lower()
#                 for word in ["learning", "learn", "studying", "study"]
#             )
#         ]

#         if learning_memories:
#             return (
#                 "Based on my saved memories, "
#                 "you are working on:\n"
#                 + "\n".join(f"- {fact}" for fact in learning_memories)
#             )

#     # 3. Favorite programming language
#     if "favorite language" in question_lower:

#         fact = find_remembered_fact("favorite language")

#         if fact:
#             return f"You said: {fact}."

#         return "I don't have your favorite language saved yet."

#     # 4. Questions about saved information
#     if any(phrase in question_lower for phrase in [
#         "what do you know about me",
#         "what do you remember about me",
#         "tell me about myself",
#         "my saved information"
#     ]):

#         if persistent_memories:
#             return (
#                 "Here is what I remember about you:\n"
#                 + "\n".join(
#                     f"- {item.get('value', '')}"
#                     for item in persistent_memories
#                 )
#             )

#         return "I don't have any saved information about you yet."

#     # 5. Find memories relevant to the question
#     relevant_memories = []

#     question_words = set(re.findall(
#         r"\b[a-zA-Z]{3,}\b",
#         question_lower
#     ))

#     ignored_words = {
#         "what", "when", "where", "which", "who",
#         "have", "does", "about", "with", "from",
#         "tell", "show", "know", "remember", "your",
#         "that", "this", "are", "you", "can"
#     }

#     question_words -= ignored_words

#     for item in persistent_memories:

#         value = item.get("value", "")
#         memory_words = set(re.findall(
#             r"\b[a-zA-Z]{3,}\b",
#             value.lower()
#         ))

#         if question_words.intersection(memory_words):
#             relevant_memories.append(value)

#     if relevant_memories:
#         return (
#             "I found some relevant information in my memory:\n"
#             + "\n".join(
#                 f"- {memory}"
#                 for memory in relevant_memories
#             )
#             + "\n\nI can use this information to help with your question."
#         )

#     # 6. Greeting
#     if "hello" in question_lower or question_lower.strip() == "hi":

#         return "Hello! I'm DevMate AI. How can I help you?"

#     # 7. Basic Python explanation
#     if "python" in question_lower:

#         return (
#             "Python is a programming language used in AI, "
#             "automation, data science, and web development."
#         )

#     # 8. Default offline response
#     return (
#         "I'm running in offline demo mode. "
#         "I can answer basic questions and use your saved memories. "
#         "Connect an AI API to enable more advanced conversations."
#     )



# # -----------------------------
# # Main Application
# # -----------------------------

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

#         # Empty input
#         if not question:

#             print("DevMate AI: Please enter a question.")
#             continue

#         intent = detect_intent(question)
#         print(f"[Router] Intent: {intent}")

#         # -------------------------
#         # Exit
#         # -------------------------

#         if intent == "exit":

#             print("DevMate AI: Goodbye! Keep learning.")
#             break

#         # -------------------------
#         # Help
#         # -------------------------

#         if intent == "help":

#             print(
#                 "Ask a question, type 'memory' to view saved memories, "
#                 "use 'remember <fact>' to save a memory, "
#                 "'clear' to reset session history, "
#                 "or 'exit' to quit."
#             )

#             continue

#         # -------------------------
#         # Custom Remember Command
#         # -------------------------

#                 # -------------------------
#         # Custom Remember Command
#         # -------------------------

#         if intent == "remember":

#             fact = question[9:].strip()

#             if not fact:
#                 print(
#                     "DevMate AI: Please tell me what to remember."
#                 )
#                 continue

#             result = save_memory(
#     "fact",
#     fact,
#     persistent_memories,
#     save_memories
# )

#             print("DevMate AI: I'll remember that.")

#             continue

#         # -------------------------
#         # Forget Memory Command
#         # -------------------------

    
#         if intent == "forget":

#             keyword = question[7:].strip()

#             if not keyword:
#                 print(
#                     "DevMate AI: Please tell me what to forget."
#                 )
#                 continue

#             removed_memories = forget_memory_tool(
#                 keyword,
#                 persistent_memories,
#                 save_memories
#             )

#             if removed_memories:
#                 print(
#                     f"DevMate AI: Removed {len(removed_memories)} memory/memories."
#                 )
#             else:
#                 print(
#                     "DevMate AI: I couldn't find a matching memory."
#                 )

#             continue


#             if removed_memories:
#                 print(
#                     f"DevMate AI: Removed {len(removed_memories)} memory."
#                 )
#             else:
#                 print(
#                     "DevMate AI: I couldn't find a matching memory."
#                 )

#             continue

       

           
#         # -------------------------
#         # Memory Command
#         # -------------------------

        
#         if intent == "memory":

#             saved = get_memories(persistent_memories)
#             print("DevMate AI: Saved memories:", saved)

#             print(
#                 f"Session history: "
#                 f"{len(conversation_history)} "
#                 f"of {MAX_HISTORY_MESSAGES} messages."
#             )

#             continue



#                 # -------------------------
#         # Clear Persistent Memory
#         # -------------------------

#         if intent == "clear_memory":

#             persistent_memories.clear()
#             save_memories(persistent_memories)

#             print(
#                 "DevMate AI: All persistent memories cleared."
#             )

#             continue

#         # -------------------------
#         # Clear Session History
#         # -------------------------

#         if intent == "clear":

#             conversation_history.clear()

#             print(
#                 "DevMate AI: Session history cleared."
#             )

#             continue

#         # -------------------------
#         # Normal Question
#         # -------------------------

#         remember("user", question)

#         try:

#             # Save name if user provides it
#             name = extract_name(question)

#             if name:

#                 # Remove previous saved name
#                 persistent_memories[:] = [
#                     memory
#                     for memory in persistent_memories
#                     if memory.get("type") != "name"
#                 ]

#                 # Save latest name
#                 persistent_memories.append({
#                     "type": "name",
#                     "value": name,
#                 })

#                 save_memories(persistent_memories)

#             # Generate response
#             answer = ask_ai(question)

#             remember("assistant", answer)

#             print("DevMate AI:", answer)

#         except Exception as error:

#             # Remove failed user message
#             conversation_history.pop()

#             print(
#                 f"Request failed: {error}"
#             )


# # -----------------------------
# # Application Entry Point
# # -----------------------------

# if __name__ == "__main__":
#     main()










import json
import os
import re

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from router import detect_intent
from tools import (
    save_memory,
    get_memories,
    forget_memory as forget_memory_tool,
)


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

MEMORY_FILE = Path(__file__).with_name("memory.json")
MAX_HISTORY_MESSAGES = 10

conversation_history = []


# ==========================================
# PERSISTENT MEMORY
# ==========================================

def load_memories():
    """Load memories from memory.json."""

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and isinstance(
            data.get("memories"), list
        ):
            return data["memories"]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_memories(memories):
    """Save memories permanently."""

    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"memories": memories},
            file,
            indent=2,
        )


persistent_memories = load_memories()


def add_memory(memory_type, value):
    """Add a new persistent memory."""

    persistent_memories[:] = load_memories()

    persistent_memories.append({
        "type": memory_type,
        "value": value,
    })

    save_memories(persistent_memories)


def forget_memory(keyword):
    """Remove memories matching a keyword."""

    persistent_memories[:] = load_memories()

    keyword = keyword.lower().strip()

    removed_memories = []

    for memory in persistent_memories[:]:

        value = str(memory.get("value", ""))

        if keyword in value.lower():

            removed_memories.append(memory)
            persistent_memories.remove(memory)

    if removed_memories:
        save_memories(persistent_memories)

    return removed_memories


# ==========================================
# NAME MEMORY
# ==========================================

def extract_name(text):
    """Extract a name from 'My name is Saikat Dey'."""

    match = re.search(
        r"\bmy name is\s+(.+)",
        text,
        re.IGNORECASE,
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
    """Find the user's saved name."""

    for memory in reversed(persistent_memories):

        value = str(memory.get("value", ""))

        if memory.get("type") == "name":
            return value

        extracted_name = extract_name(value)

        if extracted_name:
            return extracted_name

    return None


def find_remembered_fact(keyword):
    """Find a saved fact using a keyword."""

    keyword = keyword.lower()

    for memory in reversed(persistent_memories):

        if memory.get("type", "fact") == "fact":

            value = str(memory.get("value", ""))

            if keyword in value.lower():
                return value

    return None


# ==========================================
# CONVERSATION HISTORY
# ==========================================

def remember(role, content):
    """Store recent conversation messages."""

    conversation_history.append({
        "role": role,
        "content": content,
    })

    if len(conversation_history) > MAX_HISTORY_MESSAGES:
        del conversation_history[:2]


# ==========================================
# OFFLINE MEMORY SEARCH
# ==========================================

def find_relevant_memories(question):
    """Find memories related to the user's question."""

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower(),
        )
    )

    ignored_words = {
        "what", "when", "where", "which", "who",
        "have", "does", "about", "with", "from",
        "tell", "show", "know", "remember", "your",
        "that", "this", "are", "you", "can",
        "how", "why", "the", "and", "for",
        "use", "using", "help", "please",
    }

    question_words -= ignored_words

    relevant_memories = []

    for item in persistent_memories:

        value = str(item.get("value", ""))

        memory_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                value.lower(),
            )
        )

        common_words = question_words.intersection(memory_words)

        if common_words:
            relevant_memories.append(value)

    return relevant_memories


# ==========================================
# AI / OFFLINE RESPONSE
# ==========================================

def ask_ai(question):
    """Generate responses using OpenAI or offline mode."""

    # Always refresh memory from the latest JSON file.
    persistent_memories[:] = load_memories()

    question_lower = question.lower().strip()

    # --------------------------------------
    # OPENAI MODE
    # --------------------------------------

    if client is not None:

        response = client.responses.create(
            model="gpt-4.1-mini",

            instructions=(
                "You are DevMate AI, a helpful programming tutor "
                "and personal AI assistant. "
                "Use the conversation history and saved memories "
                "when relevant. "
                "Give clear, accurate and beginner-friendly answers. "
                "Never invent personal information.\n\n"
                f"Saved memories: {json.dumps(persistent_memories)}"
            ),

            input=conversation_history,
        )

        return response.output_text

    # --------------------------------------
    # OFFLINE DEMO MODE
    # --------------------------------------

    # 1. Name-related questions

    if any(phrase in question_lower for phrase in [
        "my name",
        "what is my name",
        "who am i",
    ]):

        name = extract_name(question)

        if not name:
            name = find_remembered_name()

        if name:
            return f"Your name is {name}."

        return "You haven't told me your name yet."

    # 2. Questions about learning and goals

    if any(word in question_lower for word in [
        "learning",
        "learn",
        "study",
        "studying",
        "learning goals",
    ]):

        learning_memories = [
            item.get("value", "")
            for item in persistent_memories
            if any(
                word in item.get("value", "").lower()
                for word in [
                    "learning",
                    "learn",
                    "study",
                    "studying",
                ]
            )
        ]

        if learning_memories:

            return (
                "Based on my saved memories, "
                "you are working on:\n"
                + "\n".join(
                    f"- {fact}"
                    for fact in learning_memories
                )
            )

        return "I don't have any saved learning information about you yet."

    # 3. Favorite programming language

    if "favorite language" in question_lower:

        fact = find_remembered_fact("favorite language")

        if fact:
            return f"You said: {fact}."

        return "I don't have your favorite language saved yet."

    # 4. Questions about personal information

    if any(phrase in question_lower for phrase in [
        "what do you know about me",
        "what do you remember about me",
        "tell me about myself",
        "my saved information",
    ]):

        if persistent_memories:

            return (
                "Here is what I remember about you:\n"
                + "\n".join(
                    f"- {item.get('value', '')}"
                    for item in persistent_memories
                )
            )

        return "I don't have any saved information about you yet."

    # 5. Find relevant saved memories

    relevant_memories = find_relevant_memories(question)

    if relevant_memories:

        return (
            "I found some relevant information in my memory:\n"
            + "\n".join(
                f"- {memory}"
                for memory in relevant_memories
            )
            + "\n\nI can use this information to help with your question."
        )

    # 6. Greetings

    if question_lower in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ]:

        return "Hello! I'm DevMate AI. How can I help you?"

    # 7. Basic Python explanation

    if "python" in question_lower:

        return (
            "Python is a high-level programming language "
            "used in artificial intelligence, automation, "
            "data science, machine learning and web development."
        )

    # 8. Basic JavaScript explanation

    if "javascript" in question_lower:

        return (
            "JavaScript is a programming language used to build "
            "interactive websites, web applications and backend "
            "services using technologies like Node.js."
        )

    # 9. Basic React explanation

    if "react" in question_lower:

        return (
            "React is a JavaScript library used to build "
            "interactive user interfaces using reusable components."
        )

    # 10. Default response

    return (
        "I'm currently running in offline demo mode.\n\n"
        "I can manage saved memories, retrieve personal information "
        "and answer some basic programming questions.\n\n"
        "Connect an AI API to enable advanced conversations."
    )


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    print("=" * 45)
    print("Welcome to DevMate AI!")
    print(
        "Mode:",
        "AI" if client else "Offline demo",
    )
    print("Commands: help, memory, clear, exit")
    print("=" * 45)

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

        # Detect user intent

        intent = detect_intent(question)

        print(f"[Router] Intent: {intent}")

        # --------------------------------------
        # EXIT
        # --------------------------------------

        if intent == "exit":

            print("DevMate AI: Goodbye! Keep learning.")
            break

        # --------------------------------------
        # HELP
        # --------------------------------------

        if intent == "help":

            print(
                "Ask a question, type 'memory' to view saved memories, "
                "use 'remember <fact>' to save a memory, "
                "'forget <keyword>' to delete a memory, "
                "'clear' to reset session history, "
                "or 'exit' to quit."
            )

            continue

        # --------------------------------------
        # REMEMBER
        # --------------------------------------

        if intent == "remember":

            fact = question[9:].strip()

            if not fact:

                print(
                    "DevMate AI: Please tell me what to remember."
                )

                continue

            persistent_memories[:] = load_memories()

            save_memory(
                "fact",
                fact,
                persistent_memories,
                save_memories,
            )

            print("DevMate AI: I'll remember that.")

            continue

        # --------------------------------------
        # FORGET
        # --------------------------------------

        if intent == "forget":

            keyword = question[7:].strip()

            if not keyword:

                print(
                    "DevMate AI: Please tell me what to forget."
                )

                continue

            persistent_memories[:] = load_memories()

            removed_memories = forget_memory_tool(
                keyword,
                persistent_memories,
                save_memories,
            )

            if removed_memories:

                print(
                    f"DevMate AI: Removed "
                    f"{len(removed_memories)} memory/memories."
                )

            else:

                print(
                    "DevMate AI: I couldn't find a matching memory."
                )

            continue

        # --------------------------------------
        # SHOW MEMORY
        # --------------------------------------

        if intent == "memory":

            persistent_memories[:] = load_memories()

            saved = get_memories(persistent_memories)

            print("DevMate AI: Saved memories:", saved)

            print(
                f"Session history: "
                f"{len(conversation_history)} "
                f"of {MAX_HISTORY_MESSAGES} messages."
            )

            continue

        # --------------------------------------
        # CLEAR PERSISTENT MEMORY
        # --------------------------------------

        if intent == "clear_memory":

            persistent_memories.clear()

            save_memories(persistent_memories)

            print(
                "DevMate AI: All persistent memories cleared."
            )

            continue

        # --------------------------------------
        # CLEAR SESSION HISTORY
        # --------------------------------------

        if intent == "clear":

            conversation_history.clear()

            print(
                "DevMate AI: Session history cleared."
            )

            continue

        # --------------------------------------
        # NORMAL QUESTION
        # --------------------------------------

        remember("user", question)

        try:

            # Save name when user provides it.

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

            # Generate response.

            answer = ask_ai(question)

            remember("assistant", answer)

            print("DevMate AI:", answer)

        except Exception as error:

            if conversation_history:
                conversation_history.pop()

            print(f"Request failed: {error}")


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()
