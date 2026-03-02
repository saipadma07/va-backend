import os
import google.generativeai as genai
from app.llm.base import LLMClient

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiClient(LLMClient):
    def generate(self, prompt: str) -> str:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
