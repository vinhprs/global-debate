from pydantic import BaseModel

class ChatSchema(BaseModel):
    unit: int
    prompt: str

class UserSchema(BaseModel):
    username: str
    name:str
    password:str

class LoginSchema(BaseModel):
    username: str
    password:str