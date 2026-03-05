from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    provider: str = "tinyllama"  


class ChatResponse(BaseModel):
    reply: str
    model: str
