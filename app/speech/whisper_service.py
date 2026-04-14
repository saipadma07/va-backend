import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:
    """
    Takes an audio file path and returns transcribed text
    """

    if not os.path.exists(audio_path):
        print("❌ Audio file not found")
        return ""

    try:
        result = model.transcribe(
            audio_path,
            language="en",          
            task="transcribe",      
            fp16=False              
        )

        text = result.get("text", "").strip()

        print(f"🎤 TRANSCRIPT: {text}")

        return text

    except Exception as e:
        print("❌ Whisper Error:", e)
        return ""