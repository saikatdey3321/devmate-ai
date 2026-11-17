




# import json
# import os
# import re
# from pathlib import Path

# from dotenv import load_dotenv
# from openai import OpenAI

# from router import detect_intent
# from tools import (
#     save_memory,
#     get_memories,
#     forget_memory as forget_memory_tool,
# )


# # ==========================================
# # CONFIGURATION
# # ==========================================

# load_dotenv()

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key) if api_key else None

# MEMORY_FILE = Path(__file__).with_name("memory.json")
# MAX_HISTORY_MESSAGES = 10

# conversation_history = []
# current_topic = None


# # ==========================================
# # PERSISTENT MEMORY
# # ==========================================

# def load_memories():
#     """Load memories from memory.json."""
#     try:
#         with MEMORY_FILE.open("r", encoding="utf-8") as file:
#             data = json.load(file)

#         if isinstance(data, dict) and isinstance(
#             data.get("memories"), list
#         ):
#             return data["memories"]

#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     return []


# def save_memories(memories):
#     """Save memories permanently."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump(
#             {"memories": memories},
#             file,
#             indent=2,
#         )


# persistent_memories = load_memories()


# def forget_memory(keyword):
#     """Remove memories matching a keyword."""
#     persistent_memories[:] = load_memories()

#     keyword = keyword.lower().strip()
#     removed_memories = []

#     for memory in persistent_memories[:]:
#         value = str(memory.get("value", ""))

#         if keyword in value.lower():
#             removed_memories.append(memory)
#             persistent_memories.remove(memory)

#     if removed_memories:
#         save_memories(persistent_memories)

#     return removed_memories


# # ==========================================
# # NAME MEMORY
# # ==========================================

# def extract_name(text):
#     """Extract a name from a sentence."""

#     match = re.search(
#         r"\bmy name is\s+(.+)",
#         text,
#         re.IGNORECASE,
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
#     """Find the user's saved name."""

#     persistent_memories[:] = load_memories()

#     for memory in reversed(persistent_memories):
#         value = str(memory.get("value", ""))

#         if memory.get("type") == "name":
#             return value

#         extracted_name = extract_name(value)

#         if extracted_name:
#             return extracted_name

#     return None


# # ==========================================
# # CONVERSATION HISTORY
# # ==========================================

# def remember(role, content):
#     """Store recent conversation messages."""

#     conversation_history.append({
#         "role": role,
#         "content": content,
#     })

#     if len(conversation_history) > MAX_HISTORY_MESSAGES:
#         del conversation_history[:2]


# # ==========================================
# # MEMORY HELPERS
# # ==========================================

# def find_relevant_memories(question):
#     """Find memories related to the user's question."""

#     question_words = set(
#         re.findall(
#             r"\b[a-zA-Z]{3,}\b",
#             question.lower(),
#         )
#     )

#     ignored_words = {
#         "what",
#         "when",
#         "where",
#         "which",
#         "who",
#         "have",
#         "does",
#         "about",
#         "with",
#         "from",
#         "tell",
#         "show",
#         "know",
#         "remember",
#         "your",
#         "that",
#         "this",
#         "are",
#         "you",
#         "can",
#         "how",
#         "why",
#         "the",
#         "and",
#         "for",
#         "use",
#         "using",
#         "help",
#         "please",
#         "explain",
#         "give",
#         "example",
#     }

#     question_words -= ignored_words

#     relevant_memories = []

#     for item in persistent_memories:
#         value = str(item.get("value", ""))

#         memory_words = set(
#             re.findall(
#                 r"\b[a-zA-Z]{3,}\b",
#                 value.lower(),
#             )
#         )

#         if question_words.intersection(memory_words):
#             relevant_memories.append(value)

#     return relevant_memories


# # ==========================================
# # PROGRAMMING RESPONSES
# # ==========================================

# def python_explanation():
#     return (
#         "Python is a high-level and beginner-friendly programming "
#         "language. It is popular because its syntax is easy to read "
#         "and understand.\n\n"
#         "Python is used for:\n\n"
#         "- Artificial Intelligence and Machine Learning\n"
#         "- Automation and scripting\n"
#         "- Web development\n"
#         "- Data science and data analysis\n"
#         "- Backend development\n"
#         "- Building APIs and applications"
#     )


# def python_example():
#     return """Here is a simple Python example:

# ```python
# name = "Saikat"

# print("Hello, " + name)
# ```

# ### Simple explanation

# - `name = "Saikat"` stores text in a variable called `name`.
# - `print()` displays something on the screen.
# - `"Hello, " + name` combines the greeting with the name.

# Output:

# ```text
# Hello, Saikat
# ```"""


# def another_python_example():
#     return """Here is another simple Python example:

# ```python
# age = 25

# if age >= 18:
#     print("You are an adult")
# ```

# ### Simple explanation

# - `age = 25` stores the number `25`.
# - `if age >= 18` checks whether the age is 18 or more.
# - If the condition is true, Python prints a message.

# This introduces an important programming concept called a **condition**."""


# def javascript_explanation():
#     return (
#         "JavaScript is a programming language used to make websites "
#         "interactive. It is also used for backend development with "
#         "Node.js.\n\n"
#         "JavaScript is commonly used for:\n\n"
#         "- Interactive websites\n"
#         "- Web applications\n"
#         "- Backend APIs\n"
#         "- Mobile applications\n"
#         "- Frontend frameworks such as React"
#     )


# def javascript_example():
#     return """Here is a simple JavaScript example:

# ```javascript
# const name = "Saikat";

# console.log("Hello, " + name);
# ```

# ### Simple explanation

# - `const` creates a variable.
# - `name` stores the value `"Saikat"`.
# - `console.log()` displays the result.

# Output:

# ```text
# Hello, Saikat
# ```"""


# def react_explanation():
#     return (
#         "React is a JavaScript library used to build interactive user "
#         "interfaces. React applications are built using reusable "
#         "components.\n\n"
#         "For example, a website can have separate components for:\n\n"
#         "- Navigation bar\n"
#         "- Product cards\n"
#         "- Buttons\n"
#         "- Forms\n"
#         "- Dashboard sections"
#     )


# # ==========================================
# # AI / OFFLINE RESPONSE
# # ==========================================

# def ask_ai(question):
#     """Generate responses using OpenAI or offline mode."""

#     global current_topic

#     persistent_memories[:] = load_memories()

#     question_lower = question.lower().strip()

#     # --------------------------------------
#     # OPENAI MODE
#     # --------------------------------------

#     if client is not None:

#         response = client.responses.create(
#             model="gpt-4.1-mini",
#             instructions=(
#                 "You are DevMate AI, a helpful programming tutor and "
#                 "personal AI assistant. Give clear, accurate, and "
#                 "beginner-friendly answers. Use Markdown code blocks "
#                 "for programming examples. Do not invent personal "
#                 "information.\n\n"
#                 f"Saved memories: {json.dumps(persistent_memories)}"
#             ),
#             input=conversation_history,
#         )

#         return response.output_text

#     # --------------------------------------
#     # OFFLINE MODE - GREETINGS
#     # --------------------------------------

#     if question_lower in {
#         "hi",
#         "hello",
#         "hey",
#         "good morning",
#         "good afternoon",
#         "good evening",
#     }:
#         return "Hello! I'm DevMate AI. How can I help you?"

#     # --------------------------------------
#     # PYTHON
#     # --------------------------------------

#     if "python" in question_lower:
#         current_topic = "python"

#         if (
#             "example" in question_lower
#             or "code" in question_lower
#         ):
#             return python_example()

#         return python_explanation()

#     # --------------------------------------
#     # JAVASCRIPT
#     # --------------------------------------

#     if "javascript" in question_lower:
#         current_topic = "javascript"

#         if (
#             "example" in question_lower
#             or "code" in question_lower
#         ):
#             return javascript_example()

#         return javascript_explanation()

#     # --------------------------------------
#     # REACT
#     # --------------------------------------

#     if "react" in question_lower:
#         current_topic = "react"
#         return react_explanation()

#     # --------------------------------------
#     # FOLLOW-UP: WHAT IS IT USED FOR?
#     # --------------------------------------

#     if question_lower in {
#         "what is it used for?",
#         "what is it used for",
#         "what can it be used for?",
#         "what are its uses?",
#     }:

#         if current_topic == "python":
#             return (
#                 "Python is used for:\n\n"
#                 "- Artificial Intelligence and Machine Learning\n"
#                 "- Automation and scripting\n"
#                 "- Web development\n"
#                 "- Data science and data analysis\n"
#                 "- Backend development\n"
#                 "- Building APIs and applications"
#             )

#         if current_topic == "javascript":
#             return (
#                 "JavaScript is used for:\n\n"
#                 "- Interactive websites\n"
#                 "- Frontend web applications\n"
#                 "- Backend development with Node.js\n"
#                 "- APIs\n"
#                 "- Mobile applications"
#             )

#         if current_topic == "react":
#             return (
#                 "React is mainly used for:\n\n"
#                 "- Interactive websites\n"
#                 "- Single-page applications\n"
#                 "- Dashboards\n"
#                 "- Reusable user interface components"
#             )

#         return (
#             "Please tell me which topic you are referring to."
#         )

#     # --------------------------------------
#     # FOLLOW-UP: EXAMPLE
#     # --------------------------------------

#     if question_lower in {
#         "give me an example",
#         "show me an example",
#         "give an example",
#         "show an example",
#     }:

#         if current_topic == "python":
#             return python_example()

#         if current_topic == "javascript":
#             return javascript_example()

#         return (
#             "Please tell me which programming topic you want "
#             "an example for."
#         )

#     # --------------------------------------
#     # FOLLOW-UP: ANOTHER EXAMPLE
#     # --------------------------------------

#     if question_lower in {
#         "give me another example",
#         "another example",
#         "show another example",
#     }:

#         if current_topic == "python":
#             return another_python_example()

#         if current_topic == "javascript":
#             return (
#                 "Here is another JavaScript example:\n\n"
#                 "```javascript\n"
#                 "const age = 25;\n\n"
#                 "if (age >= 18) {\n"
#                 '    console.log("You are an adult");\n'
#                 "}\n"
#                 "```\n\n"
#                 "This checks whether the person's age is 18 or older."
#             )

#         return (
#             "Please tell me which topic you want another example for."
#         )

#     # --------------------------------------
#     # FOLLOW-UP: EXPLAIN SIMPLY
#     # --------------------------------------

#     if any(
#         phrase in question_lower
#         for phrase in [
#             "explain it more simply",
#             "explain simply",
#             "make it simple",
#             "simpler explanation",
#         ]
#     ):

#         if current_topic == "python":
#             return (
#                 "Python is a simple programming language. "
#                 "You write instructions, and Python follows those "
#                 "instructions to perform tasks."
#             )

#         if current_topic == "javascript":
#             return (
#                 "JavaScript is a programming language that helps "
#                 "make websites interactive and dynamic."
#             )

#         if current_topic == "react":
#             return (
#                 "React helps developers build websites using small "
#                 "reusable pieces called components."
#             )

#         return (
#             "Please tell me which topic you want me to explain "
#             "more simply."
#         )

#     # --------------------------------------
#     # NAME QUESTIONS
#     # --------------------------------------

#     if any(
#         phrase in question_lower
#         for phrase in [
#             "my name",
#             "what is my name",
#             "who am i",
#         ]
#     ):
#         name = extract_name(question)

#         if not name:
#             name = find_remembered_name()

#         if name:
#             return f"Your name is {name}."

#         return "You haven't told me your name yet."

#     # --------------------------------------
#     # PERSONAL INFORMATION
#     # --------------------------------------

#     if any(
#         phrase in question_lower
#         for phrase in [
#             "what do you know about me",
#             "what do you remember about me",
#             "tell me about myself",
#             "my saved information",
#         ]
#     ):
#         if persistent_memories:
#             return (
#                 "Here is what I remember about you:\n\n"
#                 + "\n".join(
#                     f"- {item.get('value', '')}"
#                     for item in persistent_memories
#                 )
#             )

#         return "I don't have any saved information about you yet."

#     # --------------------------------------
#     # RELEVANT MEMORY SEARCH
#     # --------------------------------------

#     relevant_memories = find_relevant_memories(question)

#     if relevant_memories:
#         return (
#             "I found some relevant information in my memory:\n\n"
#             + "\n".join(
#                 f"- {memory}"
#                 for memory in relevant_memories
#             )
#             + "\n\nI can use this information to help with your question."
#         )

#     # --------------------------------------
#     # DEFAULT RESPONSE
#     # --------------------------------------

#     return (
#         "I'm currently running in offline demo mode.\n\n"
#         "I can manage saved memories, understand basic conversation "
#         "context, and answer programming questions.\n\n"
#         "Connect an AI API to enable more advanced conversations."
#     )


# # ==========================================
# # MAIN APPLICATION
# # ==========================================

# def main():

#     print("=" * 45)
#     print("Welcome to DevMate AI!")
#     print(
#         "Mode:",
#         "AI" if client else "Offline demo",
#     )
#     print("Commands: help, memory, clear, exit")
#     print("=" * 45)

#     while True:

#         try:
#             question = input("\nYou: ").strip()

#         except (EOFError, KeyboardInterrupt):
#             print("\nDevMate AI: Goodbye! Keep learning.")
#             break

#         if not question:
#             print("DevMate AI: Please enter a question.")
#             continue

#         intent = detect_intent(question)

#         print(f"[Router] Intent: {intent}")

#         # EXIT

#         if intent == "exit":
#             print("DevMate AI: Goodbye! Keep learning.")
#             break

#         # HELP

#         if intent == "help":
#             print(
#                 "Ask a question, type 'memory' to view saved memories, "
#                 "use 'remember <fact>' to save a memory, "
#                 "'forget <keyword>' to delete a memory, "
#                 "'clear' to reset session history, "
#                 "or 'exit' to quit."
#             )
#             continue

#         # REMEMBER

#         if intent == "remember":

#             fact = question[9:].strip()

#             if not fact:
#                 print(
#                     "DevMate AI: Please tell me what to remember."
#                 )
#                 continue

#             persistent_memories[:] = load_memories()

#             save_memory(
#                 "fact",
#                 fact,
#                 persistent_memories,
#                 save_memories,
#             )

#             print("DevMate AI: I'll remember that.")
#             continue

#         # FORGET

#         if intent == "forget":

#             keyword = question[7:].strip()

#             if not keyword:
#                 print(
#                     "DevMate AI: Please tell me what to forget."
#                 )
#                 continue

#             persistent_memories[:] = load_memories()

#             removed_memories = forget_memory_tool(
#                 keyword,
#                 persistent_memories,
#                 save_memories,
#             )

#             if removed_memories:
#                 print(
#                     f"DevMate AI: Removed "
#                     f"{len(removed_memories)} memory/memories."
#                 )
#             else:
#                 print(
#                     "DevMate AI: I couldn't find a matching memory."
#                 )

#             continue

#         # SHOW MEMORY

#         if intent == "memory":

#             persistent_memories[:] = load_memories()

#             saved = get_memories(persistent_memories)

#             print("DevMate AI: Saved memories:", saved)

#             print(
#                 f"Session history: "
#                 f"{len(conversation_history)} "
#                 f"of {MAX_HISTORY_MESSAGES} messages."
#             )

#             continue

#         # CLEAR PERSISTENT MEMORY

#         if intent == "clear_memory":

#             persistent_memories.clear()

#             save_memories(persistent_memories)

#             print(
#                 "DevMate AI: All persistent memories cleared."
#             )

#             continue

#         # CLEAR SESSION HISTORY

#         if intent == "clear":

#             conversation_history.clear()

#             print(
#                 "DevMate AI: Session history cleared."
#             )

#             continue

#         # NORMAL QUESTION

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

#             if conversation_history:
#                 conversation_history.pop()

#             print(f"Request failed: {error}")


# # ==========================================
# # APPLICATION ENTRY POINT
# # ==========================================

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


# ==================================================
# CONFIGURATION
# ==================================================

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY) if API_KEY else None

MODEL_NAME = "gpt-4.1-mini"
MEMORY_FILE = Path(__file__).with_name("memory.json")
MAX_HISTORY_MESSAGES = 10

conversation_history = []
current_topic = None


def get_ai_mode():
    """Return the currently configured AI mode."""
    return "OpenAI API" if client else "Offline"


def clear_conversation():
    """Clear the current conversation history and topic."""
    global current_topic

    conversation_history.clear()
    current_topic = None


# ==================================================
# PERSISTENT MEMORY
# ==================================================

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
    """Save memories permanently."""

    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"memories": memories},
            file,
            indent=2,
            ensure_ascii=False,
        )


persistent_memories = load_memories()


def forget_memory(keyword):
    """Remove memories matching a keyword."""

    persistent_memories[:] = load_memories()

    keyword = keyword.lower().strip()
    removed = []

    for memory in persistent_memories[:]:
        value = str(memory.get("value", ""))

        if keyword in value.lower():
            removed.append(memory)
            persistent_memories.remove(memory)

    if removed:
        save_memories(persistent_memories)

    return removed


def find_remembered_name():
    """Find the user's saved name."""

    persistent_memories[:] = load_memories()

    for memory in reversed(persistent_memories):
        if memory.get("type") == "name":
            return str(memory.get("value", ""))

    return None


def extract_name(text):
    """Extract a name from a sentence."""

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

    name = " ".join(candidate.split()[:2]).strip(" '-")

    if re.fullmatch(
        r"[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*)?",
        name,
    ):
        return name

    return None


def remember_name(name):
    """Save or update the user's name."""

    if not name:
        return

    persistent_memories[:] = load_memories()

    persistent_memories[:] = [
        item for item in persistent_memories
        if item.get("type") != "name"
    ]

    persistent_memories.append({
        "type": "name",
        "value": name,
    })

    save_memories(persistent_memories)


# ==================================================
# CONVERSATION HISTORY
# ==================================================

def remember(role, content):
    """Store recent conversation messages."""

    conversation_history.append({
        "role": role,
        "content": content,
    })

    if len(conversation_history) > MAX_HISTORY_MESSAGES:
        del conversation_history[:-MAX_HISTORY_MESSAGES]


# ==================================================
# MEMORY SEARCH
# ==================================================

def find_relevant_memories(question):
    """Find memories related to the user's question."""

    persistent_memories[:] = load_memories()

    question_words = set(
        re.findall(r"\b[a-zA-Z]{3,}\b", question.lower())
    )

    ignored_words = {
        "what", "when", "where", "which", "who",
        "have", "does", "about", "with", "from",
        "tell", "show", "know", "remember", "your",
        "that", "this", "are", "you", "can", "how",
        "why", "the", "and", "for", "use", "using",
        "help", "please", "explain", "give", "example",
    }

    question_words -= ignored_words

    relevant = []

    for item in persistent_memories:
        value = str(item.get("value", ""))

        memory_words = set(
            re.findall(r"\b[a-zA-Z]{3,}\b", value.lower())
        )

        if question_words.intersection(memory_words):
            relevant.append(value)

    return relevant


# ==================================================
# OFFLINE PROGRAMMING RESPONSES
# ==================================================

def python_explanation():
    return (
        "Python is a high-level and beginner-friendly programming "
        "language. It is popular because its syntax is easy to read.\n\n"
        "Python is used for:\n\n"
        "- Artificial Intelligence and Machine Learning\n"
        "- Automation and scripting\n"
        "- Web development\n"
        "- Data science and data analysis\n"
        "- Backend development\n"
        "- Building APIs and applications"
    )


def python_example():
    return '''Here is a simple Python example:

```python
name = "Saikat"

print("Hello, " + name)
```

### Simple explanation

- `name = "Saikat"` stores text in a variable.
- `print()` displays something on the screen.
- `"Hello, " + name` combines the greeting with the name.

Output:

```text
Hello, Saikat
```'''


def another_python_example():
    return '''Here is another Python example:

```python
age = 25

if age >= 18:
    print("You are an adult")
```

### Simple explanation

- `age = 25` stores the number 25.
- `if age >= 18` checks whether the age is 18 or more.
- If the condition is true, Python prints a message.

This introduces an important concept called a condition.'''


def javascript_explanation():
    return (
        "JavaScript is a programming language used to make websites "
        "interactive. It is also used for backend development with Node.js.\n\n"
        "JavaScript is commonly used for:\n\n"
        "- Interactive websites\n"
        "- Web applications\n"
        "- Backend APIs\n"
        "- Mobile applications\n"
        "- Frontend frameworks such as React"
    )


def javascript_example():
    return '''Here is a simple JavaScript example:

```javascript
const name = "Saikat";

console.log("Hello, " + name);
```

### Simple explanation

- `const` creates a variable.
- `name` stores the value.
- `console.log()` displays the result.

Output:

```text
Hello, Saikat
```'''


def react_explanation():
    return (
        "React is a JavaScript library used to build interactive user "
        "interfaces. React applications are built using reusable components.\n\n"
        "For example, a website can have separate components for:\n\n"
        "- Navigation bar\n"
        "- Product cards\n"
        "- Buttons\n"
        "- Forms\n"
        "- Dashboard sections"
    )


# ==================================================
# OFFLINE RESPONSE ENGINE
# ==================================================

def offline_response(question):
    """Generate a local response without an API connection."""

    global current_topic

    question_lower = question.lower().strip()

    # Greetings
    if question_lower in {
        "hi", "hello", "hey",
        "good morning", "good afternoon", "good evening",
    }:
        return "Hello! I'm DevMate AI. How can I help you?"

    # Name questions
    if any(phrase in question_lower for phrase in [
        "my name", "what is my name", "who am i",
    ]):
        name = extract_name(question) or find_remembered_name()

        if name:
            return f"Your name is {name}."

        return "You haven't told me your name yet."

    # Personal memory
    if any(phrase in question_lower for phrase in [
        "what do you know about me",
        "what do you remember about me",
        "tell me about myself",
        "my saved information",
    ]):
        memories = load_memories()

        if not memories:
            return "I don't have any saved information about you yet."

        return (
            "Here is what I remember about you:\n\n"
            + "\n".join(
                f"- {item.get('value', '')}"
                for item in memories
            )
        )

    # Python
    if "python" in question_lower:
        current_topic = "python"

        if "another example" in question_lower:
            return another_python_example()

        if "example" in question_lower or "code" in question_lower:
            return python_example()

        return python_explanation()

    # JavaScript
    if "javascript" in question_lower:
        current_topic = "javascript"

        if "another example" in question_lower:
            return '''Here is another JavaScript example:

```javascript
const age = 25;

if (age >= 18) {
    console.log("You are an adult");
}
```'''

        if "example" in question_lower or "code" in question_lower:
            return javascript_example()

        return javascript_explanation()

    # React
    if "react" in question_lower:
        current_topic = "react"

        if "example" in question_lower:
            return '''Here is a simple React example:

```jsx
function Welcome() {
    return <h1>Hello!</h1>;
}
```'''

        return react_explanation()

    # Follow-up: uses
    if any(phrase in question_lower for phrase in [
        "what is it used for",
        "what is it used",
        "what can it be used for",
        "what are its uses",
    ]):
        if current_topic == "python":
            return (
                "Python is used for:\n\n"
                "- Artificial Intelligence and Machine Learning\n"
                "- Automation and scripting\n"
                "- Web development\n"
                "- Data science\n"
                "- Backend development\n"
                "- Building APIs"
            )

        if current_topic == "javascript":
            return (
                "JavaScript is used for:\n\n"
                "- Interactive websites\n"
                "- Frontend applications\n"
                "- Backend development with Node.js\n"
                "- APIs\n"
                "- Mobile applications"
            )

        if current_topic == "react":
            return (
                "React is mainly used for building interactive websites, "
                "dashboards, and reusable user interface components."
            )

    # Follow-up: examples
    if "another example" in question_lower or question_lower == "another example":
        if current_topic == "python":
            return another_python_example()

        if current_topic == "javascript":
            return '''Here is another JavaScript example:

```javascript
const age = 25;

if (age >= 18) {
    console.log("You are an adult");
}
```'''

    if any(phrase in question_lower for phrase in [
        "give me an example",
        "show me an example",
        "show an example",
    ]):
        if current_topic == "python":
            return python_example()

        if current_topic == "javascript":
            return javascript_example()

        if current_topic == "react":
            return '''Here is a simple React example:

```jsx
function Welcome() {
    return <h1>Hello!</h1>;
}
```'''

    # Follow-up: simpler explanation
    if any(phrase in question_lower for phrase in [
        "explain it more simply",
        "explain simply",
        "make it simple",
        "simpler explanation",
    ]):
        explanations = {
            "python": (
                "Python is a simple programming language. "
                "You write instructions, and Python follows them."
            ),
            "javascript": (
                "JavaScript is a programming language that makes "
                "websites interactive and dynamic."
            ),
            "react": (
                "React helps developers build websites using small "
                "reusable pieces called components."
            ),
        }

        if current_topic in explanations:
            return explanations[current_topic]

    # Relevant memory
    relevant = find_relevant_memories(question)

    if relevant:
        return (
            "I found some relevant information in my memory:\n\n"
            + "\n".join(f"- {item}" for item in relevant)
        )

    return (
        "I'm currently running in offline mode.\n\n"
        "I can answer basic programming questions, manage saved "
        "memories, and understand simple conversation context.\n\n"
        "Configure an OpenAI API key to enable advanced AI responses."
    )


# ==================================================
# OPENAI RESPONSE ENGINE
# ==================================================

def ask_ai(question):
    """Generate an answer using OpenAI or offline mode."""

    persistent_memories[:] = load_memories()

    if client is None:
        return offline_response(question)

    instructions = (
        "You are DevMate AI, a helpful programming tutor and personal "
        "AI assistant.\n\n"
        "Teach programming concepts in a beginner-friendly way.\n"
        "Give accurate, practical explanations.\n"
        "Use Markdown formatting and fenced code blocks for code.\n"
        "Explain code examples simply.\n"
        "Keep answers clear and structured.\n"
        "Do not invent personal information about the user.\n\n"
        f"Saved user memories: {json.dumps(persistent_memories)}"
    )

    try:
        response = client.responses.create(
            model=MODEL_NAME,
            instructions=instructions,
            input=conversation_history,
        )

        answer = response.output_text

        if answer:
            return answer

        return offline_response(question)

    except Exception as error:
        print(f"OpenAI request failed: {error}")

        offline_answer = offline_response(question)

        return (
            "⚠️ OpenAI is currently unavailable. "
            "I'm answering using offline mode instead.\n\n"
            + offline_answer
        )


# ==================================================
# COMMAND LINE APPLICATION
# ==================================================

def main():

    print("=" * 45)
    print("Welcome to DevMate AI!")
    print("Mode:", get_ai_mode())
    print("Commands: help, memory, clear, clear memory, exit")
    print("=" * 45)

    while True:

        try:
            question = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nDevMate AI: Goodbye! Keep learning.")
            break

        if not question:
            print("DevMate AI: Please enter a question.")
            continue

        intent = detect_intent(question)

        print(f"[Router] Intent: {intent}")

        if intent == "exit":
            print("DevMate AI: Goodbye! Keep learning.")
            break

        if intent == "help":
            print(
                "Ask a question, type 'memory' to view saved memories, "
                "'remember <fact>' to save a memory, "
                "'forget <keyword>' to delete a memory, "
                "'clear' to reset conversation history, "
                "or 'exit' to quit."
            )
            continue

        if intent == "remember":
            fact = question[len("remember "):].strip()

            if not fact:
                print("DevMate AI: Please tell me what to remember.")
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

        if intent == "forget":
            keyword = question[len("forget "):].strip()

            if not keyword:
                print("DevMate AI: Please tell me what to forget.")
                continue

            removed = forget_memory_tool(
                keyword,
                persistent_memories,
                save_memories,
            )

            print(
                f"DevMate AI: Removed {len(removed)} memory item(s)."
                if removed
                else "DevMate AI: No matching memory found."
            )
            continue

        if intent == "memory":
            persistent_memories[:] = load_memories()

            print("DevMate AI: Saved memories:")
            print(get_memories(persistent_memories))
            print(f"Conversation messages: {len(conversation_history)}")
            continue

        if intent == "clear_memory":
            persistent_memories.clear()
            save_memories(persistent_memories)

            print("DevMate AI: All persistent memories cleared.")
            continue

        if intent == "clear":
            clear_conversation()

            print("DevMate AI: Conversation history cleared.")
            continue

        name = extract_name(question)

        if name:
            remember_name(name)

        remember("user", question)

        try:
            answer = ask_ai(question)
            remember("assistant", answer)

            print("\nDevMate AI:", answer)

        except Exception as error:
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()

            print(f"Request failed: {error}")


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================

if __name__ == "__main__":
    main()
