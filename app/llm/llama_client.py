import requests


class LlamaClient:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        # Your model
        self.model = "phi3:mini"

        self.system_prompt ="""
You are Sia, a friendly voice assistant talking to a user in real time.

Rules:
- Keep responses short (1–3 sentences).
- Speak naturally like a human friend.
- Be clear and helpful.
- If you don't know something, say you are not sure.
- Do not invent facts.
- Avoid long explanations unless the user asks.
- Answer quickly and directly.

Tone:
Warm, calm, friendly, and conversational.

Example behavior:
User: Hi
You: Hi! Nice to hear from you. How can I help today?

User: What is Python?
You: Python is a programming language used to build software, websites, and AI systems.
"""

    def generate(self, user_prompt: str) -> str:

        # Safety check
        if not user_prompt or len(user_prompt.strip()) < 3:
            return "Sorry, I didn’t quite catch that. Could you say it again?"

        prompt = f"""{self.system_prompt}

User: {user_prompt}
Sia:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,

            # Faster + stable settings
            "options": {
                "num_predict": 80,
                "temperature": 0.4,
                "top_p": 0.9,
                "num_ctx": 2048
            }
        }

        try:

            response = requests.post(
                self.url,
                json=payload,

                # ✅ VERY IMPORTANT FIX
                timeout=600
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get("response", "").strip()

            if not answer:
                return "I'm here. Could you say that again?"

            return answer


        except requests.exceptions.Timeout:
            print("⚠️ Ollama timeout")
            return "I'm thinking a bit slowly. Could you try again?"

        except Exception as e:
            print("⚠️ LLM error:", e)
            return "Sorry, I'm having a little trouble right now."