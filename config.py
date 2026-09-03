"""
Boochi configuration.
"""

# Wake word model for openWakeWord to listen for.
# Easiest option to start: use a built-in pretrained word (no training needed,
# no account needed). Options include: "hey_jarvis", "alexa", "hey_mycroft"
# This lets you test the whole pipeline right away. See README for how to
# train a real custom "Hey Boochi" model afterward.
WAKE_WORD_PATH = "hey_jarvis"

# Confidence threshold (0-1) for wake word detection. Lower = more sensitive
# (more false triggers), higher = stricter (may miss real activations).
WAKE_WORD_THRESHOLD = 0.5

# Local LLM settings (via Ollama - must have `ollama serve` running)
OLLAMA_MODEL = "llama3.2:3b"

# Whisper model size: "tiny", "base", "small" (bigger = more accurate, slower)
WHISPER_MODEL_SIZE = "base"

# How many seconds to record after the wake word fires
RECORD_SECONDS = 10
