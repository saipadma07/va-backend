import os
from groq import Groq
import base64

class VisionClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def describe(self, image_bytes: bytes):
        try:
           
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a vision assistant. "
                            "Describe ONLY what is clearly visible. "
                            "Do NOT guess, assume, or add context. "
                            "Be concise. Max 2 short sentences."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What is visible in this image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=60,   
                temperature=0.2  
            )

            answer = response.choices[0].message.content

            
            if answer:
                sentences = answer.split('. ')
                answer = '. '.join(sentences[:2]).strip()

            return answer

        except Exception as e:
            print("❌ Vision error:", e)
            return None