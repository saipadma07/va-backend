import requests


class LlamaClient:

    def __init__(self):
        """
        Runs once when the backend starts.
        Initializes model configuration and HTTP session.
        """

        # Ollama API endpoint
        self.url = "http://localhost:11434/api/generate"

        # Model name (change here if needed)
        self.model = "phi3:mini"

        # Persistent HTTP connection (faster requests)
        self.session = requests.Session()

        # System prompt controlling assistant behavior
        self.system_prompt = """
You are Sia, a friendly real-time voice assistant talking to a user.

Guidelines:
- Normally reply in 1–2 sentences.
- If the question requires explanation, give a helpful answer (3–5 sentences max).
- Speak naturally like a human friend.
- Be clear, accurate, and helpful.
- If you are unsure, say you are not sure.
- Never invent facts.

Conversation style:
- Friendly and conversational
- Direct and easy to understand
- Avoid unnecessary long explanations
"""

        # 🔥 Warm up the model once when server starts
        try:
            print("🔥 Warming up LLM model...")

            self.session.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": "Hello",
                    "stream": False
                },
                timeout=120
            )

            print("✅ LLM warmup complete")

        except Exception as e:
            print("⚠️ LLM warmup failed:", e)


    def generate(self, user_prompt: str) -> str:
        """
        Sends prompt to Ollama and returns response.
        """

        # Basic safety check
        if not user_prompt or len(user_prompt.strip()) < 2:
            return "Sorry, I didn’t quite catch that. Could you say it again?"

        # Construct final prompt
        prompt = f"{self.system_prompt}\nUser: {user_prompt}\nAssistant:"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {

                # limit response length
                "num_predict": 80,

                # reduce hallucinations
                "temperature": 0.35,

                "top_p": 0.9,

                # context window
                "num_ctx": 1024
            }
        }

        try:

            response = self.session.post(
                self.url,
                json=payload,
                timeout=180   # 🔥 increased timeout
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get("response", "").strip()

            if not answer:
                return "I'm here. Could you repeat that?"

            print("🧠 LLM RESPONSE:", answer)

            return answer


        except requests.exceptions.Timeout:
            print("⚠️ Ollama timeout")

            return "Sorry, I'm thinking a bit slowly. Could you try again?"

        except Exception as e:
            print("⚠️ LLM error:", e)

            return "Sorry, I'm having trouble answering right now."