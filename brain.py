"""
Boochi's brain: takes transcribed text, asks a local Ollama model which
tool to call, then executes it via actions.py.
"""

import ollama
import config
from actions import TOOL_REGISTRY

SYSTEM_PROMPT = """You are Boochi, a voice-controlled desktop assistant.
The user gives you a spoken command (already transcribed to text).
Decide which single tool best satisfies the command and call it with the
right arguments. If the command is just a question with no action needed
(e.g. "what's the capital of France"), answer directly in plain text
instead of calling a tool.
Always prefer calling exactly one tool per command unless the user clearly
asks for multiple separate actions.
"""

# Tool schemas in Ollama's function-calling format
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "open_browser",
            "description": "Open the default web browser to a URL",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for a query and open results",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_youtube_song",
            "description": "Search YouTube for a song or video and play the first result",
            "parameters": {
                "type": "object",
                "properties": {"song_query": {"type": "string"}},
                "required": ["song_query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_folder",
            "description": "Open a folder in File Explorer by path",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_file",
            "description": "Open a file with its default application by path",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Open a desktop application by name, e.g. notepad, calc, chrome",
            "parameters": {
                "type": "object",
                "properties": {"app_name": {"type": "string"}},
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "type_text",
            "description": "Type given text at the current cursor location",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        },
    },
]


def handle_command(command_text: str) -> str:
    """Send the transcribed command to the local LLM and execute its decision."""
    response = ollama.chat(
        model=config.OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": command_text},
        ],
        tools=TOOLS,
    )

    message = response["message"]

    # If the model called a tool, execute it
    tool_calls = message.get("tool_calls") if hasattr(message, "get") else getattr(message, "tool_calls", None)
    if tool_calls:
        results = []
        for call in tool_calls:
            if hasattr(call, "function"):
                name = call.function.name
                args = call.function.arguments
            else:
                name = call["function"]["name"]
                args = call["function"]["arguments"]

            fn = TOOL_REGISTRY.get(name)
            if fn is None:
                results.append(f"Unknown tool: {name}")
                continue
            try:
                result = fn(**args)
                results.append(result)
            except Exception as e:
                results.append(f"Error running {name}: {e}")
        return " | ".join(results)

    # Otherwise it just answered directly (e.g. a question)
    content = message.get("content", "") if hasattr(message, "get") else getattr(message, "content", "")
    return content.strip() if content else ""
