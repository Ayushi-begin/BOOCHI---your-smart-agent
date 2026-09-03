"""
Listens continuously for the "Hey Boochi" wake word using openWakeWord
(free, open-source, no account/API key needed).
Calling listen_for_wake_word() blocks until the wake word is detected, then returns.
"""

import numpy as np
import pyaudio
from openwakeword.model import Model

import config

CHUNK = 1280  # openWakeWord expects 80ms frames at 16kHz = 1280 samples
RATE = 16000


print("Loading openWakeWord model...")
oww_model = Model(
    wakeword_models=[config.WAKE_WORD_PATH],
    inference_framework="onnx",
)

def listen_for_wake_word():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=RATE,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print(f"Boochi is listening for '{config.WAKE_WORD_PATH}'...")

    try:
        while True:
            audio_data = np.frombuffer(
                stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16
            )
            prediction = oww_model.predict(audio_data)

            for model_name, score in prediction.items():
                if score > config.WAKE_WORD_THRESHOLD:
                    print(f"Wake word detected! (confidence: {score:.2f})")
                    return
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
