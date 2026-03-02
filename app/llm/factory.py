def get_llm(provider: str):
    provider = provider.lower()

    if provider == "phi3:mini":
        from app.llm.llama_client import LlamaClient
        return LlamaClient()

    elif provider == "openai":
        from app.llm.openai_client import OpenAIClient
        return OpenAIClient()

    elif provider == "gemini":
        from app.llm.gemini_client import GeminiClient
        return GeminiClient()

    else:
        raise ValueError(f"Unknown provider: {provider}")
