import whisper
import os

model = whisper.load_model("small")

def transcribe_audio(audio_path: str) -> str:
    """
    Takes an audio file path and returns transcribed text
    """
    if not os.path.exists(audio_path):
        return ""

    result = model.transcribe(audio_path)
    return result.get("text", "").strip()
