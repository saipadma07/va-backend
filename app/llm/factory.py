from app.llm.llama_client import LlamaClient


def get_llm(provider: str = "ollama"):
    provider = provider.lower()

    if provider == "ollama":
        return LlamaClient()

    else:
        raise ValueError(f"Unsupported provider: {provider}")