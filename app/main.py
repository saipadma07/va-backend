from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import uuid
import os

from app.llm.factory import get_llm
from app.speech.whisper_service import transcribe_audio
from app.speech.edge_tts_service import text_to_speech


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMP_DIR = BASE_DIR / "temp"

STATIC_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

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

# Load LLM ONCE (good)
llm = get_llm("tinyllama")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def health():
    return {"status": "ok"}


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


@app.post("/chat")
async def chat(req: ChatRequest):
    answer = llm.generate(req.prompt)
    return {"answer": answer}


@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    temp_audio = TEMP_DIR / f"{uuid.uuid4()}.webm"

    try:
        with open(temp_audio, "wb") as f:
            f.write(await file.read())

        transcript = transcribe_audio(str(temp_audio))
        transcript = (transcript or "").strip()

        print("TRANSCRIPT:", transcript)

        # 🔒 Guard against garbage / silence
        if len(transcript) < 3:
            fallback_text = "Sorry, I didn’t catch that. Could you please repeat?"

            audio_url = await text_to_speech(fallback_text)

            return {
                "transcript": transcript,
                "answer": fallback_text,
                "audio_url": audio_url
            }

        answer = llm.generate(transcript)
        print("ANSWER:", answer)

        audio_url = await text_to_speech(answer)
        print("AUDIO URL:", audio_url)

        return {
            "transcript": transcript,
            "answer": answer,
            "audio": audio_url
        }

    finally:
        if temp_audio.exists():
            temp_audio.unlink()
