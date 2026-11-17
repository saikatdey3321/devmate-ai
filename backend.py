


# import json
# from pathlib import Path

# from app import ask_ai, remember, clear_conversation
# from tools import forget_memory


# MEMORY_FILE = Path(__file__).with_name("memory.json")

# conversation_context = {
#     "topic": None,
# }


# # ==================================================
# # MEMORY MANAGEMENT
# # ==================================================

# def load_memories():
#     """Load persistent memories."""

#     try:
#         with MEMORY_FILE.open("r", encoding="utf-8") as file:
#             data = json.load(file)

#         if isinstance(data, dict) and isinstance(data.get("memories"), list):
#             return data["memories"]

#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     return []


# def save_memories(memories):
#     """Save persistent memories."""

#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump(
#             {"memories": memories},
#             file,
#             indent=2,
#             ensure_ascii=False,
#         )


# def normalize_memory(value):
#     """Normalize memory text for duplicate checking."""

#     value = str(value).strip().lower()

#     if value.startswith("that "):
#         value = value[5:].strip()

#     return value


# def get_memory_summary(memories):
#     """Create a readable memory summary."""

#     if not memories:
#         return "I don't have any saved memories about you yet."

#     return "\n".join(
#         f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
#         for item in memories
#     )


# def add_memory(value, memory_type="fact"):
#     """Save a memory without creating duplicates."""

#     value = value.strip()

#     if not value:
#         return "Please tell me what you want me to remember."

#     memories = load_memories()
#     normalized_value = normalize_memory(value)

#     for item in memories:
#         if normalize_memory(item.get("value", "")) == normalized_value:
#             return "I already have that memory saved."

#     memories.append({
#         "type": memory_type,
#         "value": value,
#     })

#     save_memories(memories)

#     return f"I'll remember: {value}"


# def remove_memory(keyword):
#     """Remove memories matching a keyword."""

#     memories = load_memories()

#     if not keyword.strip():
#         return "Please tell me which memory you want me to forget."

#     removed = forget_memory(
#         keyword.strip(),
#         memories,
#         save_memories,
#     )

#     if not removed:
#         return f"I couldn't find a memory matching '{keyword}'."

#     return f"Forgot {len(removed)} matching memory item(s)."


# # ==================================================
# # CONVERSATION MANAGEMENT
# # ==================================================

# def reset_conversation():
#     """Reset conversation history and topic context."""

#     conversation_context["topic"] = None
#     clear_conversation()


# def detect_topic(text):
#     """Detect the programming topic."""

#     lowered = text.lower()

#     if "javascript" in lowered or "node.js" in lowered:
#         return "javascript"

#     if "python" in lowered:
#         return "python"

#     if "react" in lowered:
#         return "react"

#     return None


# def get_current_topic():
#     """Return the current conversation topic."""

#     return conversation_context.get("topic")


# # ==================================================
# # FOLLOW-UP RESPONSES
# # ==================================================

# def get_follow_up_response(question):
#     """Generate responses using the current conversation topic."""

#     lowered = question.lower().strip()
#     topic = get_current_topic()

#     if not topic:
#         return None

#     # ---------------- PYTHON ----------------

#     if topic == "python":

#         if any(phrase in lowered for phrase in [
#             "give me another example",
#             "another example",
#             "show another example",
#         ]):
#             return '''Here is another Python example:

# ```python
# age = 25

# if age >= 18:
#     print("You are an adult")
# ```

# ### Simple explanation

# - `age = 25` stores the number 25.
# - `if age >= 18` checks whether age is 18 or greater.
# - Python prints the message when the condition is true.'''

#         if any(phrase in lowered for phrase in [
#             "give me an example",
#             "show me an example",
#             "show an example",
#         ]):
#             return '''Here is a simple Python example:

# ```python
# name = "Saikat"

# print("Hello, " + name)
# ```

# This code stores a name and prints a greeting.'''

#         if any(phrase in lowered for phrase in [
#             "what is it used for",
#             "what is it used",
#             "where is it used",
#             "uses of it",
#             "its uses",
#         ]):
#             return '''Python is used for:

# - Artificial Intelligence and Machine Learning
# - Automation and scripting
# - Web development
# - Data science and data analysis
# - Backend development
# - Building APIs and applications'''

#         if any(phrase in lowered for phrase in [
#             "explain it more simply",
#             "explain more simply",
#             "simplify it",
#             "explain simply",
#             "simple explanation",
#         ]):
#             return (
#                 "Python is a simple and beginner-friendly programming "
#                 "language. You write instructions, and Python follows "
#                 "those instructions to perform tasks."
#             )

#         if any(phrase in lowered for phrase in [
#             "why should i learn it",
#             "why learn it",
#             "why should i learn python",
#         ]):
#             return (
#                 "You should learn Python because it is beginner-friendly, "
#                 "powerful, widely used, and important for automation, "
#                 "AI, data science, and backend development."
#             )

#     # ---------------- JAVASCRIPT ----------------

#     if topic == "javascript":

#         if any(phrase in lowered for phrase in [
#             "another example",
#             "show another example",
#         ]):
#             return '''Here is another JavaScript example:

# ```javascript
# const age = 25;

# if (age >= 18) {
#     console.log("You are an adult");
# }
# ```'''

#         if "example" in lowered:
#             return '''Here is a simple JavaScript example:

# ```javascript
# const name = "Saikat";

# console.log("Hello, " + name);
# ```'''

#         if any(phrase in lowered for phrase in [
#             "what is it used for",
#             "what is it used",
#             "where is it used",
#         ]):
#             return '''JavaScript is mainly used for:

# - Interactive websites
# - Frontend development
# - Backend development with Node.js
# - Web applications
# - Mobile applications'''

#         if any(phrase in lowered for phrase in [
#             "explain simply",
#             "explain it more simply",
#             "simplify it",
#         ]):
#             return (
#                 "JavaScript is a programming language that makes "
#                 "websites interactive and dynamic."
#             )

#     # ---------------- REACT ----------------

#     if topic == "react":

#         if any(phrase in lowered for phrase in [
#             "another example",
#             "show another example",
#         ]):
#             return '''Here is another React example:

# ```jsx
# function Button() {
#     return <button>Click Me</button>;
# }
# ```'''

#         if "example" in lowered:
#             return '''Here is a simple React example:

# ```jsx
# function Welcome() {
#     return <h1>Hello!</h1>;
# }
# ```'''

#         if any(phrase in lowered for phrase in [
#             "what is it used for",
#             "what is it used",
#             "where is it used",
#         ]):
#             return (
#                 "React is mainly used for building interactive user "
#                 "interfaces, websites, dashboards, and web applications."
#             )

#         if any(phrase in lowered for phrase in [
#             "explain simply",
#             "explain it more simply",
#             "simplify it",
#         ]):
#             return (
#                 "React helps developers build websites using small "
#                 "reusable pieces called components."
#             )

#     return None


# # ==================================================
# # MAIN BACKEND RESPONSE
# # ==================================================

# def get_response(question):
#     """Process a user question and return an assistant response."""

#     text = question.strip()
#     lowered = text.lower()

#     if not text:
#         return "Please enter a question."

#     memories = load_memories()

#     # ---------------- SHOW MEMORIES ----------------

#     if lowered in {
#         "show memories",
#         "list memories",
#         "what do you remember?",
#         "what do you remember about me?",
#         "what do you know about me?",
#         "my saved memories",
#     }:
#         return get_memory_summary(memories)

#     # ---------------- PERSONAL MEMORY QUESTIONS ----------------

#     personal_questions = {
#         "what am i learning?",
#         "what are my learning goals?",
#         "what are my goals?",
#         "what have i told you about myself?",
#     }

#     if lowered in personal_questions:

#         if not memories:
#             return "I don't have any saved information about you yet."

#         return (
#             "Based on my saved memories, here's what I know:\n\n"
#             + get_memory_summary(memories)
#         )

#     # ---------------- SAVE MEMORY ----------------

#     if lowered.startswith("remember "):
#         value = text[len("remember "):].strip()

#         return add_memory(value)

#     # ---------------- FORGET MEMORY ----------------

#     if lowered.startswith("forget "):
#         keyword = text[len("forget "):].strip()

#         return remove_memory(keyword)

#     # ---------------- DETECT TOPIC ----------------

#     detected_topic = detect_topic(text)

#     if detected_topic:
#         conversation_context["topic"] = detected_topic

#     # ---------------- FOLLOW-UP RESPONSE ----------------

#     follow_up_answer = get_follow_up_response(text)

#     if follow_up_answer:
#         remember("user", text)
#         remember("assistant", follow_up_answer)

#         return follow_up_answer

#     # ---------------- NORMAL AI RESPONSE ----------------

#     remember("user", text)

#     answer = ask_ai(text)

#     remember("assistant", answer)

#     return answer



from app import remember, clear_conversation
from agent import run_agent
from pathlib import Path
import json


MEMORY_FILE = Path(__file__).with_name("memory.json")

conversation_context = {
    "topic": None,
}


# ==================================================
# MEMORY MANAGEMENT
# ==================================================

def load_memories():
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and isinstance(data.get("memories"), list):
            return data["memories"]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_memories(memories):
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"memories": memories},
            file,
            indent=2,
            ensure_ascii=False,
        )


def normalize_memory(value):
    value = str(value).strip().lower()

    if value.startswith("that "):
        value = value[5:].strip()

    return value


def get_memory_summary(memories):
    if not memories:
        return "I don't have any saved memories about you yet."

    return "\n".join(
        f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
        for item in memories
    )


def add_memory(value):
    if not value.strip():
        return "Please tell me what you want me to remember."

    memories = load_memories()
    normalized = normalize_memory(value)

    for item in memories:
        if normalize_memory(item.get("value", "")) == normalized:
            return "I already have that memory saved."

    memories.append({
        "type": "fact",
        "value": value.strip(),
    })

    save_memories(memories)

    return f"I'll remember: {value}"


def remove_memory(keyword):
    if not keyword.strip():
        return "Please tell me which memory you want me to forget."

    memories = load_memories()
    removed = []

    for memory in memories[:]:
        value = str(memory.get("value", ""))

        if keyword.lower() in value.lower():
            removed.append(memory)
            memories.remove(memory)

    if removed:
        save_memories(memories)
        return f"Forgot {len(removed)} matching memory item(s)."

    return f"I couldn't find a memory matching '{keyword}'."


# ==================================================
# CONVERSATION MANAGEMENT
# ==================================================

def reset_conversation():
    conversation_context["topic"] = None
    clear_conversation()


def detect_topic(text):
    lowered = text.lower()

    if "javascript" in lowered or "node.js" in lowered:
        return "javascript"

    if "python" in lowered:
        return "python"

    if "react" in lowered:
        return "react"

    return None


def get_current_topic():
    return conversation_context.get("topic")


# ==================================================
# FOLLOW-UP RESPONSES
# ==================================================

def get_follow_up_response(question):
    lowered = question.lower().strip()
    topic = get_current_topic()

    if not topic:
        return None

    # Python
    if topic == "python":

        if "another example" in lowered:
            return '''Here is another Python example:

```python
age = 25

if age >= 18:
    print("You are an adult")
```

Explanation:
- age = 25 stores a number.
- if checks a condition.
- print displays the result.'''

        if "example" in lowered:
            return '''Here is a Python example:

```python
name = "Saikat"
print("Hello, " + name)
```'''

        if any(phrase in lowered for phrase in [
            "what is it used for",
            "what is it used",
            "where is it used",
            "its uses",
        ]):
            return '''Python is used for:

- Artificial Intelligence
- Automation
- Web development
- Data science
- Backend development
- API development'''

        if "explain simply" in lowered or "simplify it" in lowered:
            return (
                "Python is a beginner-friendly programming language "
                "used to give instructions to a computer."
            )

    # JavaScript
    if topic == "javascript":

        if "another example" in lowered:
            return '''Here is another JavaScript example:

```javascript
const age = 25;

if (age >= 18) {
    console.log("You are an adult");
}
```'''

        if "example" in lowered:
            return '''Here is a JavaScript example:

```javascript
const name = "Saikat";
console.log("Hello, " + name);
```'''

        if any(phrase in lowered for phrase in [
            "what is it used for",
            "what is it used",
            "where is it used",
        ]):
            return '''JavaScript is used for:

- Interactive websites
- Frontend development
- Backend development
- APIs
- Mobile applications'''

    # React
    if topic == "react":

        if "another example" in lowered:
            return '''Here is another React example:

```jsx
function Button() {
    return <button>Click Me</button>;
}
```'''

        if "example" in lowered:
            return '''Here is a React example:

```jsx
function Welcome() {
    return <h1>Hello!</h1>;
}
```'''

        if any(phrase in lowered for phrase in [
            "what is it used for",
            "what is it used",
            "where is it used",
        ]):
            return (
                "React is used to build interactive websites, "
                "dashboards and reusable UI components."
            )

    return None


# ==================================================
# MAIN BACKEND RESPONSE
# ==================================================

def get_response(question):
    text = question.strip()
    lowered = text.lower()

    if not text:
        return "Please enter a question."

    memories = load_memories()

    # Show memories
    if lowered in {
        "show memories",
        "list memories",
        "what do you remember?",
        "what do you remember about me?",
        "what do you know about me?",
        "my saved memories",
    }:
        return get_memory_summary(memories)

    # Personal memory questions
    if lowered in {
        "what am i learning?",
        "what are my learning goals?",
        "what are my goals?",
        "what have i told you about myself?",
    }:
        return get_memory_summary(memories)

    # Remember command
    if lowered.startswith("remember "):
        value = text[len("remember "):].strip()

        if value.lower().startswith("that "):
            value = value[5:].strip()

        return add_memory(value)

    # Forget command
    if lowered.startswith("forget "):
        keyword = text[len("forget "):].strip()
        return remove_memory(keyword)

    # Detect topic
    detected_topic = detect_topic(text)

    if detected_topic:
        conversation_context["topic"] = detected_topic

    # Handle local follow-ups
    follow_up_answer = get_follow_up_response(text)

    if follow_up_answer:
        remember("user", text)
        remember("assistant", follow_up_answer)

        return follow_up_answer

    # Normal agent response
    remember("user", text)

    answer = run_agent(
        question=text,
        history=list(__import__("app").conversation_history),
    )

    remember("assistant", answer)

    return answer
