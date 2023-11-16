import datetime
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Các biến cấu hình
SECRET_KEY = "your_secret_key"
SALT_TOKEN = SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Cấu hình Passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hàm tạo token
def create_access_token(data: dict, expires_delta: datetime.timedelta):
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2PasswordBearer cho FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Hàm xác thực token
def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    if token == None:
        raise credentials_exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("name")
        mail: str = payload.get("mail")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    # except jwt.JWTError:
    #     raise credentials_exception
    return username, token, mail


# Các hàm khác ở đây giữ nguyên như trước
def generate_token(mail: str, name: str):
    payload = {
        "mail": mail,
        "name": name,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
