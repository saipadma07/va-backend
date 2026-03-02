import asyncio
import edge_tts
import uuid
from pathlib import Path

# Save audio here
AUDIO_DIR = Path("app/static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:

    text = text.strip()

    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    # Keep responses short for speed
    return text[:300]


async def text_to_speech(text: str):

    try:

        text = clean_text(text)

        file_path = AUDIO_DIR / f"{uuid.uuid4()}.mp3"

        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-JennyNeural",
            rate="+0%",
            pitch="+0Hz"
        )

        # Slightly larger timeout
        await asyncio.wait_for(
            communicate.save(str(file_path)),
            timeout=12
        )

        return f"/static/audio/{file_path.name}"

    except Exception as e:

        print("⚠️ Edge TTS failed:", e)

        return None