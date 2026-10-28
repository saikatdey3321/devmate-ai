

# from app import ask_ai, remember, conversation_history
# from tools import save_memory, get_memories, forget_memory
# import json
# from pathlib import Path


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
#     """Persist memories to memory.json."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump({"memories": memories}, file, indent=2)


# def get_response(question):
#     """Process a question and return a DevMate AI response."""
#     text = question.strip()
#     lowered = text.lower()
#     memories = load_memories()

#     if lowered in {"show memories", "list memories", "what do you remember?"}:
#         if not memories:
#             return "I don't have any saved memories yet."

#         return "\n".join(
#             f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
#             for item in memories
#         )

#     if lowered.startswith("remember "):
#         value = text[len("remember "):].strip()

#         if not value:
#             return "Please tell me what you want me to remember."

#         new_memory = {"type": "fact", "value": value}

#         if new_memory in memories:
#             return "I already have that memory saved."

#         memories = save_memory(
#             "fact", value, memories, save_memories
#         ) if False else memories

#         memories.append(new_memory)
#         save_memories(memories)

#         return f"I'll remember: {value}"

#     if lowered.startswith("forget "):
#         keyword = text[len("forget "):].strip()

#         if not keyword:
#             return "Please tell me which memory you want me to forget."

#         removed = forget_memory(keyword, memories, save_memories)

#         if not removed:
#             return f"I couldn't find a memory matching '{keyword}'."

#         return f"Forgot {len(removed)} matching memory item(s)."

#     remember("user", text)
#     answer = ask_ai(text)
#     remember("assistant", answer)

#     return answer





import json
from pathlib import Path

from app import ask_ai, remember
from tools import forget_memory


MEMORY_FILE = Path(__file__).with_name("memory.json")


def load_memories():
    """Load saved memories from memory.json."""
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
    """Persist memories to memory.json."""
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump({"memories": memories}, file, indent=2)


def normalize_memory(value):
    """Normalize text to help identify duplicate memories."""
    value = str(value).strip().lower()

    if value.startswith("that "):
        value = value[5:].strip()

    return value


def get_memory_summary(memories):
    """Create a readable summary of saved memories."""
    if not memories:
        return "I don't have any saved memories about you yet."

    return "\n".join(
        f"- [{item.get('type', 'fact')}] {item.get('value', '')}"
        for item in memories
    )


def get_response(question):
    """Process chat messages and use saved memories when relevant."""
    text = question.strip()
    lowered = text.lower()
    memories = load_memories()

    # Show all saved memories
    if lowered in {
        "show memories",
        "list memories",
        "what do you remember?",
        "what do you remember about me?",
        "what do you know about me?",
    }:
        return get_memory_summary(memories)

    # Answer personal learning-goal questions using saved memories
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

    # Save a memory
    if lowered.startswith("remember "):
        value = text[len("remember "):].strip()

        if value.lower().startswith("that "):
            value = value[5:].strip()

        if not value:
            return "Please tell me what you want me to remember."

        normalized_value = normalize_memory(value)

        for item in memories:
            if (
                item.get("type", "fact") == "fact"
                and normalize_memory(item.get("value", ""))
                == normalized_value
            ):
                return "I already have that memory saved."

        memories.append({
            "type": "fact",
            "value": value,
        })
        save_memories(memories)

        return f"I'll remember: {value}"

    # Forget matching memories
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

    # Handle normal questions
    remember("user", text)
    answer = ask_ai(text)
    remember("assistant", answer)

    return answer
