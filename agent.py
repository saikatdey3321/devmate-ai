
import ast
import json
import operator
from pathlib import Path

from app import client, MODEL_NAME, ask_ai
from tools import save_memory


MEMORY_FILE = Path(__file__).with_name("memory.json")

MAX_TOOL_ROUNDS = 5


# ==================================================
# TOOL 1: CALCULATOR
# ==================================================

def calculator(expression):
    """Safely calculate basic mathematical expressions."""

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported mathematical operation.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = allowed_operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation.")

            return operation(evaluate(node.operand))

        raise ValueError("Invalid mathematical expression.")

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree.body)

    return {
        "expression": expression,
        "result": result,
    }


# ==================================================
# TOOL 2: SEARCH MEMORY
# ==================================================

def search_memory(keyword):
    """Search persistent memories."""

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        memories = data.get("memories", [])

    except (FileNotFoundError, json.JSONDecodeError):
        memories = []

    keyword = keyword.lower().strip()

    matches = [
        memory
        for memory in memories
        if keyword in str(memory.get("value", "")).lower()
    ]

    return {
        "count": len(matches),
        "memories": matches,
    }


# ==================================================
# TOOL 3: SAVE MEMORY
# ==================================================

def remember_information(memory_type, value):
    """Save information into persistent memory."""

    if not value.strip():
        return {"success": False, "message": "Memory cannot be empty."}

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        memories = data.get("memories", [])

    except (FileNotFoundError, json.JSONDecodeError):
        memories = []

    normalized = value.strip().lower()

    for memory in memories:
        if (
            memory.get("type", "fact") == memory_type
            and str(memory.get("value", "")).strip().lower() == normalized
        ):
            return {
                "success": True,
                "message": "This information is already saved.",
            }

    result = save_memory(
        memory_type,
        value.strip(),
        memories,
        save_memories,
    )

    return {
        "success": True,
        "message": result,
    }


def save_memories(memories):
    """Persist memories to JSON."""

    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"memories": memories},
            file,
            indent=2,
            ensure_ascii=False,
        )


# ==================================================
# TOOL 4: PYTHON CODE ANALYZER
# ==================================================

def analyze_python_code(code):
    """Check Python code for syntax errors without executing it."""

    try:
        ast.parse(code)

        return {
            "valid": True,
            "message": "Python syntax is valid.",
        }

    except SyntaxError as error:
        return {
            "valid": False,
            "message": error.msg,
            "line": error.lineno,
            "column": error.offset,
        }


# ==================================================
# TOOL REGISTRY
# ==================================================

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "search_memory": search_memory,
    "remember_information": remember_information,
    "analyze_python_code": analyze_python_code,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "calculator",
        "description": "Calculate a mathematical expression. Use this tool when the user asks for a calculation.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression, for example 25 * 4 + 10.",
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "search_memory",
        "description": "Search the user's saved memories for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Keyword to search for in saved memories.",
                }
            },
            "required": ["keyword"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "remember_information",
        "description": "Save information when the user explicitly asks you to remember it.",
        "parameters": {
            "type": "object",
            "properties": {
                "memory_type": {
                    "type": "string",
                    "enum": ["fact", "name", "preference"],
                },
                "value": {
                    "type": "string",
                    "description": "Information to save.",
                },
            },
            "required": ["memory_type", "value"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "analyze_python_code",
        "description": "Check Python code for syntax errors without running the code.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Python source code to check.",
                }
            },
            "required": ["code"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


# ==================================================
# TOOL EXECUTION
# ==================================================

def execute_tool(name, arguments):
    """Find and execute a registered tool."""

    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        return {
            "success": False,
            "error": f"Unknown tool: {name}",
        }

    try:
        result = function(**arguments)

        return {
            "success": True,
            "result": result,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ==================================================
# AGENT EXECUTION LOOP
# ==================================================

def run_agent(question, history=None):
    """
    Run the AI agent.

    The agent can select tools, execute them,
    inspect results, and continue reasoning.
    """

    # Offline fallback
    if client is None:
        return ask_ai(question)

    instructions = """
You are DevMate AI, an intelligent programming and developer assistant.

You are an AI agent capable of using tools.

Your responsibilities:

1. Understand the user's request.
2. Decide whether a tool is necessary.
3. Select the appropriate tool when needed.
4. Execute the tool and inspect its result.
5. Use tool results to provide an accurate answer.
6. Continue using tools when necessary, but never exceed the tool limit.
7. Never claim that a tool was executed unless it actually succeeded.

Available tools:

- calculator: Perform mathematical calculations.
- search_memory: Search saved user information.
- remember_information: Save information when explicitly requested.
- analyze_python_code: Check Python syntax without executing code.

Safety rules:

- Never execute arbitrary Python code.
- Never invent tool results.
- Do not save personal information unless the user explicitly requests it.
- Explain errors clearly.
- Keep answers beginner-friendly and structured.
"""

    conversation = history if history else [
        {"role": "user", "content": question}
    ]

    try:

        response = client.responses.create(
            model=MODEL_NAME,
            instructions=instructions,
            input=conversation,
            tools=TOOL_DEFINITIONS,
        )

        # Agent tool execution loop
        for _ in range(MAX_TOOL_ROUNDS):

            function_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not function_calls:
                return response.output_text or (
                    "I couldn't generate a response."
                )

            tool_outputs = []

            for call in function_calls:

                try:
                    arguments = json.loads(call.arguments)

                    result = execute_tool(
                        call.name,
                        arguments,
                    )

                except (json.JSONDecodeError, TypeError) as error:
                    result = {
                        "success": False,
                        "error": f"Invalid tool arguments: {error}",
                    }

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result, ensure_ascii=False),
                })

            response = client.responses.create(
                model=MODEL_NAME,
                previous_response_id=response.id,
                input=tool_outputs,
                tools=TOOL_DEFINITIONS,
            )

        return (
            "I reached the maximum number of tool execution rounds. "
            "Please try breaking the task into smaller steps."
        )

    except Exception as error:

        print(f"Agent error: {error}")

        return (
            "⚠️ The AI agent encountered an error. "
            "I'm switching to offline mode.\n\n"
            + ask_ai(question)
        )
