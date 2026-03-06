import requests


class LlamaClient:

    def __init__(self):
        """
        Runs once when the backend starts.
        We initialize the model configuration and HTTP session here.
        """

        # Ollama API endpoint
        self.url = "http://localhost:11434/api/generate"

        # Model name
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

Examples:

User: Hi
Sia: Hi! Nice to hear from you. How can I help today?

User: What is Python?
Sia: Python is a popular programming language used to build software, websites, and AI systems. It’s known for being easy to learn and very versatile.

User: Explain neural networks
Sia: Neural networks are computer models inspired by the human brain. They process information through layers of connected nodes called neurons. Each layer learns patterns in data, allowing systems to recognize things like images, speech, or text.
"""


    def generate(self, user_prompt: str) -> str:
        """
        Sends a prompt to Ollama and returns the generated response.
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

                # Limits response length (faster)
                "num_predict": 80,

                # Lower randomness = fewer hallucinations
                "temperature": 0.35,

                "top_p": 0.9,

                # Context window (kept small for speed)
                "num_ctx": 1024
            }
        }

        try:

            response = self.session.post(
                self.url,
                json=payload,
                timeout=60
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