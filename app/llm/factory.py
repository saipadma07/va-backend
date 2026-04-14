import os
from app.llm.llama_client import LlamaClient
from app.llm.groq_client import GroqClient


def get_llm(provider: str = None):
    """
    Factory to return the correct LLM client.
    Defaults to GROQ (recommended).
    """

    provider = (provider or os.getenv("LLM_PROVIDER", "groq")).lower()

    if provider == "groq":
        print("✅ Using GROQ LLM")
        return GroqClient()

    elif provider == "ollama":
        print("⚠️ Using Ollama LLM")
        return LlamaClient()

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")