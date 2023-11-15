import jwt
import datetime
from starlette.config import Config
from passlib.context import CryptContext

env = Config(".env")

SECRET_KEY = env("SECRET_KEY", cast=str)

SALT_TOKEN = env("SALT_TOKEN", cast=str, default=SECRET_KEY)


def generate_token(name: str):
    SECRET_KEY = "your_secret_key"
    payload = {
        "123": name,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=1),  
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
