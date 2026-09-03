import pyttsx3

# Initialize the pyttsx3 engine once globally
engine = pyttsx3.init()

def speak(text: str):
    """Speak the given text using the offline TTS engine."""
    if not text:
        return
        
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Failed to speak: {e}")
