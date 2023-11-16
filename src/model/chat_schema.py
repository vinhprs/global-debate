from pydantic import BaseModel, EmailStr, constr


class ChatSchema(BaseModel):
    unit_id: int = 1
    prompt: str = ""
    topic_id: int = 1


class UserSchema(BaseModel):
    username: constr(min_length=3, strip_whitespace=True)
    email: EmailStr
    password: constr(min_length=5, strip_whitespace=True)


class LoginSchema(BaseModel):
    username: constr(min_length=3, strip_whitespace=True)
    password: constr(min_length=5, strip_whitespace=True)
