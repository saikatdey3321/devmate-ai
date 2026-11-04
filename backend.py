



# # import json
# # from pathlib import Path

# # from app import ask_ai, remember
# # from tools import forget_memory


# # MEMORY_FILE = Path(__file__).with_name("memory.json")


# # def load_memories():
# #     """Load saved memories from memory.json."""
# #     try:
# #         with MEMORY_FILE.open("r", encoding="utf-8") as file:
# #             data = json.load(file)

# #         if isinstance(data, dict) and isinstance(
# #             data.get("memories"), list
# #         ):
# #             return data["memories"]

# #     except (FileNotFoundError, json.JSONDecodeError):
# #         pass

# #     return []


# # def save_memories(memories):
# #     """Persist memories to memory.json."""
# #     with MEMORY_FILE.open("w", encoding="utf-8") as file:
# #         json.dump({"memories": memories}, file, indent=2)


# # def normalize_memory(value):
# #     """Normalize text to help identify duplicate memories."""
# #     value = str(value).strip().lower()

# #     if value.startswith("that "):
# #         value = value[5:].strip()

# #     return value


# # def get_memory_summary(memories):
# #     """Create a readable summary of saved memories."""
# #     if not memories:
# #         return "I don't have any saved memories about you yet."

# #     return "\n".join(
# #         f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
# #         for item in memories
# #     )


# # def get_response(question):
# #     """Process chat messages and use saved memories when relevant."""
# #     text = question.strip()
# #     lowered = text.lower()
# #     memories = load_memories()

# #     # Show all saved memories
# #     if lowered in {
# #         "show memories",
# #         "list memories",
# #         "what do you remember?",
# #         "what do you remember about me?",
# #         "what do you know about me?",
# #     }:
# #         return get_memory_summary(memories)

# #     # Answer personal learning-goal questions using saved memories
# #     personal_questions = {
# #         "what am i learning?",
# #         "what are my learning goals?",
# #         "what are my goals?",
# #         "what have i told you about myself?",
# #     }

# #     if lowered in personal_questions:
# #         if not memories:
# #             return "I don't have any saved information about you yet."

# #         return (
# #             "Based on my saved memories, here's what I know:\n\n"
# #             + get_memory_summary(memories)
# #         )

# #     # Save a memory
# #     if lowered.startswith("remember "):
# #         value = text[len("remember "):].strip()

# #         if value.lower().startswith("that "):
# #             value = value[5:].strip()

# #         if not value:
# #             return "Please tell me what you want me to remember."

# #         normalized_value = normalize_memory(value)

# #         for item in memories:
# #             if (
# #                 item.get("type", "fact") == "fact"
# #                 and normalize_memory(item.get("value", ""))
# #                 == normalized_value
# #             ):
# #                 return "I already have that memory saved."

# #         memories.append({
# #             "type": "fact",
# #             "value": value,
# #         })
# #         save_memories(memories)

# #         return f"I'll remember: {value}"

# #     # Forget matching memories
# #     if lowered.startswith("forget "):
# #         keyword = text[len("forget "):].strip()

# #         if not keyword:
# #             return "Please tell me which memory you want me to forget."

# #         removed = forget_memory(
# #             keyword,
# #             memories,
# #             save_memories,
# #         )

# #         if not removed:
# #             return f"I couldn't find a memory matching '{keyword}'."

# #         return f"Forgot {len(removed)} matching memory item(s)."

# #     # Handle normal questions using saved memory context
# # remember("user", text)

# # if memories:
# #     memory_context = "\n".join(
# #         f"- {item.get('value', '')}"
# #         for item in memories
# #     )

# #     contextual_question = f"""
# # You are DevMate AI, a helpful programming assistant.

# # Here is some information remembered about the user:
# # {memory_context}

# # Use these memories only when relevant to the user's question.
# # Do not invent personal information.

# # User question:
# # {text}
# # """

# # else:
# #     contextual_question = text

# # answer = ask_ai(contextual_question)

# # remember("assistant", answer)

# # return answer




# import json
# from pathlib import Path

# from app import ask_ai, remember
# from tools import forget_memory


# MEMORY_FILE = Path(__file__).with_name("memory.json")


# def load_memories():
#     """Load saved memories from memory.json."""
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
#     """Save memories to memory.json."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump({"memories": memories}, file, indent=2)


# def normalize_memory(value):
#     """Normalize text to identify duplicate memories."""
#     value = str(value).strip().lower()

#     if value.startswith("that "):
#         value = value[5:].strip()

#     return value


# def get_memory_summary(memories):
#     """Create a readable summary of saved memories."""
#     if not memories:
#         return "I don't have any saved memories about you yet."

#     return "\n".join(
#         f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
#         for item in memories
#     )


# def get_response(question):
#     """Process chat messages and use saved memories."""

#     text = question.strip()
#     lowered = text.lower()
#     memories = load_memories()

#     # Show saved memories
#     if lowered in {
#         "show memories",
#         "list memories",
#         "what do you remember?",
#         "what do you remember about me?",
#         "what do you know about me?",
#     }:
#         return get_memory_summary(memories)

#     # Answer personal questions using saved memories
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

#     # Save a memory
#     if lowered.startswith("remember "):
#         value = text[len("remember "):].strip()

#         if value.lower().startswith("that "):
#             value = value[5:].strip()

#         if not value:
#             return "Please tell me what you want me to remember."

#         normalized_value = normalize_memory(value)

#         for item in memories:
#             if (
#                 item.get("type", "fact") == "fact"
#                 and normalize_memory(item.get("value", ""))
#                 == normalized_value
#             ):
#                 return "I already have that memory saved."

#         memories.append({
#             "type": "fact",
#             "value": value,
#         })

#         save_memories(memories)

#         return f"I'll remember: {value}"

#     # Forget matching memories
#     if lowered.startswith("forget "):
#         keyword = text[len("forget "):].strip()

#         if not keyword:
#             return "Please tell me which memory you want me to forget."

#         removed = forget_memory(
#             keyword,
#             memories,
#             save_memories,
#         )

#         if not removed:
#             return f"I couldn't find a memory matching '{keyword}'."

#         return f"Forgot {len(removed)} matching memory item(s)."

#     # Handle normal questions using saved memory context
#     remember("user", text)

#     if memories:
#         memory_context = "\n".join(
#             f"- {item.get('value', '')}"
#             for item in memories
#         )

#         contextual_question = f"""
# You are DevMate AI, a helpful programming assistant.

# Here is some information remembered about the user:
# {memory_context}

# Use these memories only when relevant to the user's question.
# Do not invent personal information.

# User question:
# {text}
# """
#     else:
#         contextual_question = text

#     answer = ask_ai(contextual_question)

#     remember("assistant", answer)

#     return answer







# import json
# from pathlib import Path

# from app import ask_ai, remember
# from tools import forget_memory


# MEMORY_FILE = Path(__file__).with_name("memory.json")

# # Store the current conversation topic for follow-up questions
# conversation_context = {
#     "topic": None
# }


# def load_memories():
#     """Load saved memories from memory.json."""
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
#     """Save memories to memory.json."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump({"memories": memories}, file, indent=2)


# def normalize_memory(value):
#     """Normalize text to identify duplicate memories."""
#     value = str(value).strip().lower()

#     if value.startswith("that "):
#         value = value[5:].strip()

#     return value


# def get_memory_summary(memories):
#     """Create a readable summary of saved memories."""
#     if not memories:
#         return "I don't have any saved memories about you yet."

#     return "\n".join(
#         f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
#         for item in memories
#     )


# def detect_topic(text):
#     """Detect the programming topic from the user's message."""
#     lowered = text.lower()

#     if "python" in lowered:
#         return "python"

#     if "javascript" in lowered:
#         return "javascript"

#     if "react" in lowered:
#         return "react"

#     return None


# def get_follow_up_response(question):
#     """Handle simple follow-up questions using conversation context."""
#     lowered = question.lower().strip()
#     topic = conversation_context.get("topic")

#     if not topic:
#         return None

#     # Python follow-up questions
#     if topic == "python":

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "what is it used for",
#                 "what is it used",
#                 "where is it used",
#                 "uses of it",
#                 "its uses",
#             ]
#         ):
#             return (
#                 "Python is used for:\n\n"
#                 "- Artificial Intelligence and Machine Learning\n"
#                 "- Automation and scripting\n"
#                 "- Web development\n"
#                 "- Data science and data analysis\n"
#                 "- Backend development\n"
#                 "- Building APIs and applications"
#             )

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "give me an example",
#                 "show me an example",
#                 "example",
#             ]
#         ):
#             return (
#                 "Here is a simple Python example:\n\n"
#                 "```python\n"
#                 "name = 'Saikat'\n"
#                 "print('Hello, ' + name)\n"
#                 "```\n\n"
#                 "This code stores a name in a variable and prints a greeting."
#             )

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "explain it more simply",
#                 "explain more simply",
#                 "simplify it",
#                 "simple explanation",
#             ]
#         ):
#             return (
#                 "Python is a simple and beginner-friendly programming "
#                 "language. You write instructions, and Python executes "
#                 "those instructions to perform tasks."
#             )

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "why should i learn it",
#                 "why learn it",
#                 "why should i learn python",
#             ]
#         ):
#             return (
#                 "You should learn Python because it is beginner-friendly, "
#                 "powerful, widely used, and very important for automation, "
#                 "AI, data science, and backend development."
#             )

#     # JavaScript follow-up questions
#     if topic == "javascript":

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "what is it used for",
#                 "what is it used",
#                 "where is it used",
#             ]
#         ):
#             return (
#                 "JavaScript is mainly used for:\n\n"
#                 "- Interactive websites\n"
#                 "- Frontend development\n"
#                 "- Backend development with Node.js\n"
#                 "- Web applications\n"
#                 "- Mobile applications"
#             )

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "give me an example",
#                 "show me an example",
#                 "example",
#             ]
#         ):
#             return (
#                 "Here is a simple JavaScript example:\n\n"
#                 "```javascript\n"
#                 "const name = 'Saikat';\n"
#                 "console.log(`Hello, ${name}`);\n"
#                 "```"
#             )

#     # React follow-up questions
#     if topic == "react":

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "what is it used for",
#                 "what is it used",
#                 "where is it used",
#             ]
#         ):
#             return (
#                 "React is mainly used for building interactive user "
#                 "interfaces, websites, dashboards, and web applications "
#                 "using reusable components."
#             )

#         if any(
#             phrase in lowered
#             for phrase in [
#                 "give me an example",
#                 "show me an example",
#                 "example",
#             ]
#         ):
#             return (
#                 "Here is a simple React component:\n\n"
#                 "```jsx\n"
#                 "function Welcome() {\n"
#                 "    return <h1>Hello!</h1>;\n"
#                 "}\n"
#                 "```"
#             )

#     return None


# def get_response(question):
#     """Process chat messages using memory and conversation context."""

#     text = question.strip()
#     lowered = text.lower()
#     memories = load_memories()

#     # --------------------------------------
#     # SHOW SAVED MEMORIES
#     # --------------------------------------

#     if lowered in {
#         "show memories",
#         "list memories",
#         "what do you remember?",
#         "what do you remember about me?",
#         "what do you know about me?",
#     }:
#         return get_memory_summary(memories)

#     # --------------------------------------
#     # PERSONAL QUESTIONS
#     # --------------------------------------

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

#     # --------------------------------------
#     # SAVE MEMORY
#     # --------------------------------------

#     if lowered.startswith("remember "):
#         value = text[len("remember "):].strip()

#         if value.lower().startswith("that "):
#             value = value[5:].strip()

#         if not value:
#             return "Please tell me what you want me to remember."

#         normalized_value = normalize_memory(value)

#         for item in memories:
#             if (
#                 item.get("type", "fact") == "fact"
#                 and normalize_memory(item.get("value", ""))
#                 == normalized_value
#             ):
#                 return "I already have that memory saved."

#         memories.append({
#             "type": "fact",
#             "value": value,
#         })

#         save_memories(memories)

#         return f"I'll remember: {value}"

#     # --------------------------------------
#     # FORGET MEMORY
#     # --------------------------------------

#     if lowered.startswith("forget "):
#         keyword = text[len("forget "):].strip()

#         if not keyword:
#             return "Please tell me which memory you want me to forget."

#         removed = forget_memory(
#             keyword,
#             memories,
#             save_memories,
#         )

#         if not removed:
#             return f"I couldn't find a memory matching '{keyword}'."

#         return f"Forgot {len(removed)} matching memory item(s)."

#     # --------------------------------------
#     # DETECT NEW CONVERSATION TOPIC
#     # --------------------------------------

#     detected_topic = detect_topic(text)

#     if detected_topic:
#         conversation_context["topic"] = detected_topic

#     # --------------------------------------
#     # CHECK FOLLOW-UP CONTEXT
#     # --------------------------------------

#     follow_up_answer = get_follow_up_response(text)

#     if follow_up_answer:
#         remember("user", text)
#         remember("assistant", follow_up_answer)

#         return follow_up_answer

#     # --------------------------------------
#     # NORMAL AI QUESTION
#     # --------------------------------------

#     remember("user", text)

#     answer = ask_ai(text)

#     remember("assistant", answer)

#     return answer



import json
from pathlib import Path

from app import ask_ai, remember
from tools import forget_memory


MEMORY_FILE = Path(__file__).with_name("memory.json")

conversation_context = {
    "topic": None,
}


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
        json.dump({"memories": memories}, file, indent=2)


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


def detect_topic(text):
    lowered = text.lower()

    if "python" in lowered:
        return "python"

    if "javascript" in lowered:
        return "javascript"

    if "react" in lowered:
        return "react"

    return None


def get_follow_up_response(question):
    lowered = question.lower().strip()
    topic = conversation_context.get("topic")

    if not topic:
        return None

    # Python follow-up questions
    if topic == "python":

        if any(
            phrase in lowered
            for phrase in [
                "give me another example",
                "another example",
                "show another example",
            ]
        ):
            return """Here is another Python example:

```python
age = 25

if age >= 18:
    print("You are an adult")
```

Simple explanation:

- `age = 25` stores the number 25.
- `if age >= 18` checks whether age is 18 or greater.
- Python prints the message when the condition is true."""

        if any(
            phrase in lowered
            for phrase in [
                "give me an example",
                "show me an example",
                "show an example",
            ]
        ):
            return """Here is a simple Python example:

```python
name = "Saikat"

print("Hello, " + name)
```

This code stores a name and prints a greeting."""

        if any(
            phrase in lowered
            for phrase in [
                "what is it used for",
                "what is it used",
                "where is it used",
                "uses of it",
                "its uses",
            ]
        ):
            return """Python is used for:

- Artificial Intelligence and Machine Learning
- Automation and scripting
- Web development
- Data science and data analysis
- Backend development
- Building APIs and applications"""

        if any(
            phrase in lowered
            for phrase in [
                "explain it more simply",
                "explain more simply",
                "simplify it",
                "explain simply",
                "simple explanation",
            ]
        ):
            return (
                "Python is a simple and beginner-friendly programming "
                "language. You write instructions, and Python follows "
                "those instructions to perform tasks."
            )

        if any(
            phrase in lowered
            for phrase in [
                "why should i learn it",
                "why learn it",
                "why should i learn python",
            ]
        ):
            return (
                "You should learn Python because it is beginner-friendly, "
                "powerful, widely used, and important for automation, "
                "AI, data science, and backend development."
            )

    # JavaScript follow-up questions
    if topic == "javascript":

        if "another example" in lowered:
            return """Here is another JavaScript example:

```javascript
const age = 25;

if (age >= 18) {
    console.log("You are an adult");
}
```"""

        if "example" in lowered:
            return """Here is a simple JavaScript example:

```javascript
const name = "Saikat";

console.log("Hello, " + name);
```"""

        if any(
            phrase in lowered
            for phrase in [
                "what is it used for",
                "what is it used",
                "where is it used",
            ]
        ):
            return """JavaScript is mainly used for:

- Interactive websites
- Frontend development
- Backend development with Node.js
- Web applications
- Mobile applications"""

    # React follow-up questions
    if topic == "react":

        if "another example" in lowered:
            return """Here is another React example:

```jsx
function Button() {
    return <button>Click Me</button>;
}
```"""

        if "example" in lowered:
            return """Here is a simple React example:

```jsx
function Welcome() {
    return <h1>Hello!</h1>;
}
```"""

        if any(
            phrase in lowered
            for phrase in [
                "what is it used for",
                "what is it used",
                "where is it used",
            ]
        ):
            return (
                "React is mainly used for building interactive user "
                "interfaces, websites, dashboards, and web applications."
            )

    return None


def get_response(question):
    text = question.strip()
    lowered = text.lower()
    memories = load_memories()

    # Show memories
    if lowered in {
        "show memories",
        "list memories",
        "what do you remember?",
        "what do you remember about me?",
        "what do you know about me?",
    }:
        return get_memory_summary(memories)

    # Personal memory questions
    personal_questions = {
        "what am i learning?",
        "what are my learning goals?",
        "what are my goals?",
        "what have i told you about myself?",
    }

    if lowered in personal_questions:
        if not memories:
            return "I don't have any saved information about you yet."

        return (
            "Based on my saved memories, here's what I know:\n\n"
            + get_memory_summary(memories)
        )

    # Save memory
    if lowered.startswith("remember "):
        value = text[len("remember "):].strip()

        if value.lower().startswith("that "):
            value = value[5:].strip()

        if not value:
            return "Please tell me what you want me to remember."

        normalized_value = normalize_memory(value)

        for item in memories:
            if normalize_memory(item.get("value", "")) == normalized_value:
                return "I already have that memory saved."

        memories.append(
            {
                "type": "fact",
                "value": value,
            }
        )

        save_memories(memories)

        return f"I'll remember: {value}"

    # Forget memory
    if lowered.startswith("forget "):
        keyword = text[len("forget "):].strip()

        if not keyword:
            return "Please tell me which memory you want me to forget."

        removed = forget_memory(
            keyword,
            memories,
            save_memories,
        )

        if not removed:
            return f"I couldn't find a memory matching '{keyword}'."

        return f"Forgot {len(removed)} matching memory item(s)."

    # Detect conversation topic
    detected_topic = detect_topic(text)

    if detected_topic:
        conversation_context["topic"] = detected_topic

    # Handle follow-up question
    follow_up_answer = get_follow_up_response(text)

    if follow_up_answer:
        remember("user", text)
        remember("assistant", follow_up_answer)

        return follow_up_answer

    # Normal AI response
    remember("user", text)

    answer = ask_ai(text)

    remember("assistant", answer)

    return answer