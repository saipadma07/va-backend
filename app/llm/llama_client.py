import requests


class LlamaClient:

    def __init__(self):
        """
        Local Ollama LLM client (fallback mode).
        """

        self.url = "http://localhost:11434/api/generate"

        self.model = "phi3:mini"

        self.session = requests.Session()

        self.system_prompt = """
You are Sia, a friendly real-time voice assistant.

Guidelines:
- Reply in 1–2 sentences normally
- If needed, explain clearly (max 3–5 sentences)
- Be natural and conversational
- Be accurate, do not hallucinate
- If unsure, say you don’t know
"""

        try:
            print("🔥 Warming up Ollama model...")

            self.session.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": "Hello",
                    "stream": False
                },
                timeout=60
            )

            print("✅ Ollama warmup complete")

        except Exception as e:
            print("⚠️ Ollama warmup failed:", e)

    def generate(self, user_prompt: str) -> str:
        """
        Generate response using Ollama.
        """

        if not user_prompt or len(user_prompt.strip()) < 2:
            return "Sorry, I didn’t catch that. Could you repeat?"

        prompt = f"{self.system_prompt}\n\nUser: {user_prompt}\nAssistant:"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 80,
                "temperature": 0.4,
                "top_p": 0.9,
                "num_ctx": 1024
            }
        }

        try:
            response = self.session.post(
                self.url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            data = response.json()
            answer = data.get("response", "").strip()

            if not answer:
                return "I'm here. Could you repeat that?"

            print("🧠 Ollama RESPONSE:", answer)

            return answer

        except requests.exceptions.Timeout:
            print("⚠️ Ollama timeout")
            return "Sorry, I'm taking too long. Try again."

        except Exception as e:
            print("⚠️ Ollama error:", e)
            return "Sorry, something went wrong."