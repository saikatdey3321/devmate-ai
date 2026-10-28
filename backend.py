

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
    """Normalize memory text for duplicate comparisons."""
    value = str(value).strip().lower()

    if value.startswith("that "):
        value = value[5:].strip()

    return value


def get_response(question):
    """Process a question and return a DevMate AI response."""
    text = question.strip()
    lowered = text.lower()
    memories = load_memories()

    # Show saved memories
    if lowered in {
        "show memories",
        "list memories",
        "what do you remember?",
    }:
        if not memories:
            return "I don't have any saved memories yet."

        return "\n".join(
            f"- [{item.get('type', 'fact')}] "
            f"{item.get('value', '')}"
            for item in memories
        )

    # Save a memory
    if lowered.startswith("remember "):
        value = text[len("remember "):].strip()

        if not value:
            return "Please tell me what you want me to remember."

        value = (
            value[5:].strip()
            if value.lower().startswith("that ")
            else value
        )

        if not value:
            return "Please tell me what you want me to remember."

        normalized_value = normalize_memory(value)

        for item in memories:
            if (
                item.get("type", "fact") == "fact"
                and normalize_memory(item.get("value", ""))
                == normalized_value
            ):
                return "This memory is already saved."

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

    # Normal chat response
    remember("user", text)
    answer = ask_ai(text)
    remember("assistant", answer)

    return answer

