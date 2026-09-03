"""
Boochi's toolbox: real actions it can take on the computer.
Each function is exposed to the LLM as a callable tool.
"""

import os
import time
import subprocess
import webbrowser
import urllib.parse

try:
    import pyautogui
except ImportError:
    pyautogui = None  # allow the module to load even before pyautogui is installed


def open_browser(url: str = "https://www.google.com"):
    """Open the default web browser to a given URL."""
    webbrowser.open(url)
    return f"Opened browser to {url}"


def web_search(query: str):
    """Search Google for a query and open the results in the browser."""
    q = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?q={q}")
    return f"Searched the web for: {query}"


def play_youtube_song(song_query: str):
    """Search YouTube for a song/video and auto-play the first result."""
    q = urllib.parse.quote(song_query)
    webbrowser.open(f"https://www.youtube.com/results?search_query={q}")

    if pyautogui is not None:
        # Give the page time to load, then click the first video thumbnail.
        # NOTE: thumbnail position varies by screen resolution/zoom - you may
        # need to tune these coordinates or switch to an image-based click.
        time.sleep(3.5)
        pyautogui.click(x=300, y=300)  # rough position of first result

    return f"Playing '{song_query}' on YouTube"


def open_folder(path: str):
    """Open a folder in File Explorer."""
    path = os.path.expandvars(os.path.expanduser(path))
    if not os.path.exists(path):
        return f"Folder not found: {path}"
    os.startfile(path)
    return f"Opened folder: {path}"


def open_file(path: str):
    """Open a file with its default associated application."""
    path = os.path.expandvars(os.path.expanduser(path))
    if not os.path.exists(path):
        return f"File not found: {path}"
    os.startfile(path)
    return f"Opened file: {path}"


def open_application(app_name: str):
    """Open a Windows application by name (e.g. 'notepad', 'calc', 'chrome')."""
    try:
        subprocess.Popen(app_name)
        return f"Opened {app_name}"
    except FileNotFoundError:
        return f"Could not find application: {app_name}"


def type_text(text: str):
    """Type text at the current cursor location (e.g. dictation into a doc/email)."""
    if pyautogui is None:
        return "pyautogui not installed - cannot type text"
    time.sleep(0.5)
    pyautogui.write(text, interval=0.02)
    return f"Typed: {text}"


# Registry mapping tool names -> functions, used by brain.py
TOOL_REGISTRY = {
    "open_browser": open_browser,
    "web_search": web_search,
    "play_youtube_song": play_youtube_song,
    "open_folder": open_folder,
    "open_file": open_file,
    "open_application": open_application,
    "type_text": type_text,
}
