from pydantic import BaseModel

class ChatSchema(BaseModel):
    unit_id: int = 1
    prompt: str = ""
    topic_id: int = 1

class UserSchema(BaseModel):
    username: str
    name:str
    password:str

class LoginSchema(BaseModel):
    username: str
    password:str