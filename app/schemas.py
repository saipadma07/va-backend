from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    provider: str = "phi3:mini"  


class ChatResponse(BaseModel):
    reply: str
    model: str
