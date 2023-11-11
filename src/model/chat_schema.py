from pydantic import BaseModel

class ChatSchema(BaseModel):
    unit: int
    prompt: str