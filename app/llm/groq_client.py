import os
from groq import Groq
import traceback

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found")

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        print(f"✅ Groq initialized with model: {self.model}")

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Sia, a smart and helpful AI assistant. "
                            "Give SHORT and DIRECT answers. "
                            "Limit response to 2–3 sentences MAX. "
                            "Do NOT over-explain. "
                            "Do NOT guess or assume unknown information. "
                            "If unsure, say 'I’m not sure.'"
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,   
                max_tokens=80      
            )

            result = response.choices[0].message.content.strip()

            
            if result:
                sentences = result.split('. ')
                result = '. '.join(sentences[:2]).strip()

            print("✅ GROQ RESPONSE:", result)

            return result

        except Exception as e:
            print("❌ Groq FULL ERROR:")
            traceback.print_exc()
            return "Sorry, I couldn't process that."