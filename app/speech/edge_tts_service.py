import edge_tts
import uuid
from pathlib import Path

AUDIO_DIR = Path("app/static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = text.strip()

    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    return text[:300]


async def text_to_speech(text: str):
    try:
        text = clean_text(text)

        filename = f"{uuid.uuid4()}.mp3"
        file_path = AUDIO_DIR / filename

        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-JennyNeural"
        )

        # ✅ NO wait_for (important fix)
        await communicate.save(str(file_path))

        print("✅ Audio saved:", file_path)

        return f"/static/audio/{filename}"

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("⚠️ Edge TTS failed:", e)
        return None