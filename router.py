def detect_intent(command):
    """Detect the user's intended command."""

    command = command.lower().strip()

    if command in ("exit", "quit"):
        return "exit"

    if command == "help":
        return "help"

    if command == "memory":
        return "memory"

    if command == "clear":
        return "clear"

    if command == "clear memory":
        return "clear_memory"

    if command.startswith("remember "):
        return "remember"

    if command.startswith("forget "):
        return "forget"

    return "chat"