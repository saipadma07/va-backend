from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import uuid
import os
import requests
import base64

from app.llm.factory import get_llm
from app.speech.whisper_service import transcribe_audio
from app.speech.edge_tts_service import text_to_speech


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMP_DIR = BASE_DIR / "temp"

STATIC_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "audio").mkdir(exist_ok=True)  # ensure audio folder exists

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LLM ONCE
llm = get_llm("ollama")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def health():
    return {"status": "ok"}


# ==============================
# SPEECH TO TEXT
# ==============================

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    temp_audio = TEMP_DIR / f"{uuid.uuid4()}.webm"

    try:
        with open(temp_audio, "wb") as f:
            f.write(await file.read())

        transcript = transcribe_audio(str(temp_audio))

        return {"text": transcript}

    finally:
        if temp_audio.exists():
            temp_audio.unlink()


# ==============================
# CHAT
# ==============================

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = llm.generate(req.prompt)
    return {"answer": answer}


# ==============================
# VOICE CHAT
# ==============================

@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    temp_audio = TEMP_DIR / f"{uuid.uuid4()}.webm"

    try:
        with open(temp_audio, "wb") as f:
            f.write(await file.read())

        transcript = transcribe_audio(str(temp_audio))
        transcript = (transcript or "").strip()

        print("TRANSCRIPT:", transcript)

        if len(transcript) < 3:
            fallback_text = "Sorry, I didn’t catch that. Could you please repeat?"

            audio_url = await text_to_speech(fallback_text)

            return {
                "transcript": transcript,
                "answer": fallback_text,
                "audio": audio_url   # ✅ fixed key
            }

        answer = llm.generate(transcript)
        print("ANSWER:", answer)

        audio_url = await text_to_speech(answer)

        return {
            "transcript": transcript,
            "answer": answer,
            "audio": audio_url
        }

    finally:
        if temp_audio.exists():
            temp_audio.unlink()


# ==============================
# 🔥 VISION (NEW FEATURE)
# ==============================

def describe_image(image_path):
    """
    Uses LLaVA (Ollama) to describe the image
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llava",
            "prompt": "Describe this image clearly.",
            "images": [image_base64],
            "stream": False
        }
    )

    data = response.json()
    return data.get("response", "").strip()


@app.post("/vision-chat")
async def vision_chat(file: UploadFile = File(...)):
    temp_image = TEMP_DIR / f"{uuid.uuid4()}.jpg"

    try:
        # Save uploaded image
        with open(temp_image, "wb") as f:
            f.write(await file.read())

        print("🖼 Image received")

        # Step 1: Describe image
        description = describe_image(str(temp_image))
        print("IMAGE DESCRIPTION:", description)

        # Step 2: Ask LLM to explain
        answer = llm.generate(
            f"The user is showing an image. Description: {description}. Explain it simply."
        )

        print("VISION ANSWER:", answer)

        # Step 3: Convert to speech
        audio_url = await text_to_speech(answer)

        return {
            "description": description,
            "answer": answer,
            "audio": audio_url
        }

    finally:
        if temp_image.exists():
            temp_image.unlink()