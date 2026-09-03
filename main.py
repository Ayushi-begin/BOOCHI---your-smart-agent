"""
Boochi - voice-controlled desktop agent.
Run this with `python main.py` (after Ollama is running and config.py is filled in).
"""

import pyaudio
import wave
import tempfile
import os

from faster_whisper import WhisperModel

import config
from wake_word import listen_for_wake_word
from brain import handle_command
from tts import speak

print("Loading Whisper model...")
whisper_model = WhisperModel(config.WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")


def record_command(seconds=config.RECORD_SECONDS) -> str:
    """Record a few seconds of audio to a temp WAV file and return its path."""
    chunk = 1024
    fmt = pyaudio.paInt16
    channels = 1
    rate = 16000

    pa = pyaudio.PyAudio()
    stream = pa.open(format=fmt, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print(f"Listening for your command ({seconds}s)...")
    frames = []
    for _ in range(int(rate / chunk * seconds)):
        frames.append(stream.read(chunk, exception_on_overflow=False))

    stream.stop_stream()
    stream.close()
    pa.terminate()

    tmp_path = os.path.join(tempfile.gettempdir(), "boochi_command.wav")
    wf = wave.open(tmp_path, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(pa.get_sample_size(fmt))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    return tmp_path


def transcribe(wav_path: str) -> str:
    segments, _ = whisper_model.transcribe(wav_path)
    text = " ".join(seg.text for seg in segments).strip()
    return text


def main():
    print("Boochi is starting up...")
    while True:
        listen_for_wake_word()
        wav_path = record_command()
        command_text = transcribe(wav_path)

        if not command_text:
            print("Didn't catch that - try again.")
            continue

        print(f"Heard: {command_text}")
        result = handle_command(command_text)
        print(f"Boochi: {result}")
        speak(result)


if __name__ == "__main__":
    main()
