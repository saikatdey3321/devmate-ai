def tool_status():
    """Return a simple status message from the tool system."""
    return "Tool system is working."


def save_memory(memory_type, value, memories, save_callback):
    """Save a memory using the provided memory store."""
    memories.append({
        "type": memory_type,
        "value": value
    })

    save_callback(memories)

    return f"Saved memory: {value}"

def get_memories(memories):
    """Return all saved memories."""
    return memories

def forget_memory(keyword, memories, save_callback):
    """Remove memories containing the given keyword."""
    keyword = keyword.lower()
    removed_memories = []

    for memory in memories[:]:
        value = str(memory.get("value", ""))

        if keyword in value.lower():
            removed_memories.append(memory)
            memories.remove(memory)

    if removed_memories:
        save_callback(memories)

    return removed_memories