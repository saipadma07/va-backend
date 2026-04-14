from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import uuid
import os
import base64

from dotenv import load_dotenv
from groq import Groq

import cv2
import numpy as np

from app.llm.factory import get_llm
from app.llm.vision_client import VisionClient
from app.speech.whisper_service import transcribe_audio
from app.speech.edge_tts_service import text_to_speech

# ============================
# INIT
# ============================
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

app = FastAPI()

STATIC_DIR = BASE_DIR / "static"
TEMP_DIR = BASE_DIR / "temp"

STATIC_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "audio").mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = get_llm()
vision_client = VisionClient()

latest_vision_description = None

class ChatRequest(BaseModel):
    prompt: str

# ============================
# IMAGE PREPROCESSING (🔥 SPEED BOOST)
# ============================
def preprocess_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 🔥 resize (BIGGEST BOOST)
    frame = cv2.resize(frame, (320, 240))

    # 🔥 compress
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

    return buffer.tobytes()

# ============================
# HEALTH
# ============================
@app.get("/")
def health():
    return {"status": "ok"}

# ============================
# TEXT CHAT
# ============================
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        answer = llm.generate(req.prompt)
        audio_url = await text_to_speech(answer)

        return {
            "answer": answer,
            "audio": audio_url
        }

    except Exception as e:
        return {
            "answer": str(e),
            "audio": None
        }

# ============================
# VOICE CHAT
# ============================
@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    global latest_vision_description

    temp_audio = TEMP_DIR / f"{uuid.uuid4()}.wav"

    try:
        with open(temp_audio, "wb") as f:
            f.write(await file.read())

        transcript = transcribe_audio(str(temp_audio))
        transcript = (transcript or "").strip()

        print("🎤 TRANSCRIPT:", transcript)

        if len(transcript) < 2:
            fallback = "Sorry, I didn’t catch that. Please repeat."
            audio_url = await text_to_speech(fallback)

            return {
                "transcript": transcript,
                "answer": fallback,
                "audio": audio_url
            }

        if latest_vision_description:
            prompt = f"""
You are Sia.

User said:
{transcript}

Camera sees:
{latest_vision_description}

Reply briefly in 1-2 sentences. Do not guess.
"""
        else:
            prompt = f"""
You are Sia.

User said:
{transcript}

Reply briefly in 1-2 sentences.
"""

        answer = llm.generate(prompt)
        audio_url = await text_to_speech(answer)

        return {
            "transcript": transcript,
            "answer": answer,
            "audio": audio_url
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "transcript": "",
            "answer": str(e),
            "audio": None
        }

    finally:
        if temp_audio.exists():
            temp_audio.unlink()

# ============================
# VISION ANALYSIS (🔥 FIXED)
# ============================
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    global latest_vision_description

    try:
        raw_bytes = await file.read()

        # 🔥 FAST preprocessing
        image_bytes = preprocess_image(raw_bytes)

        # 🔥 Groq Vision
        description = vision_client.describe(image_bytes)

        print("👁️ VISION:", description)

        if not description:
            return {
                "description": "Vision failed",
                "answer": "Could not analyze image",
                "audio": None
            }

        latest_vision_description = description

        # 🔥 SHORT + ACCURATE PROMPT
        prompt = f"""
You are Sia.

Camera sees:
{description}

Explain briefly in 1-2 sentences. Do not guess.
"""

        answer = llm.generate(prompt)
        audio_url = await text_to_speech(answer)

        return {
            "description": description,
            "answer": answer,
            "audio": audio_url
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "description": "Error",
            "answer": str(e),
            "audio": None
        }