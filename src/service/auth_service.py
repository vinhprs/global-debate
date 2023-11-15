import json
import src.middleware.authen as Authen
from src.utils.mongodb_utils import DB_MONGO
import requests


def authen(username: str, password: str):
    # user = get_user()
    COLLECTION_USER = DB_MONGO["user"]
    myquery = {"username": username}
    user_data = COLLECTION_USER.find_one(myquery)
    if user_data:
        if Authen.verify_password(password, user_data["password"]):
            token = Authen.generate_token(name=user_data["name"])
            return user_data["name"], token
    return None


def get_user(username: str):
    COLLECTION_USER = DB_MONGO["user"]
    myquery = {"username": username}
    user_data = COLLECTION_USER.find_one(myquery)
    return user_data


def register(name: str, username: str, password: str):
    COLLECTION_USER = DB_MONGO["user"]
    myquery = {"username": username}
    user_data = COLLECTION_USER.find_one(myquery)
    if user_data:
        return None
    passWord = Authen.get_password_hash(password)
    userData = {"username": username, "name": name, "password": passWord}
    token = Authen.generate_token(name=name)
    COLLECTION_USER.insert_one(userData)
    return name, token


def loginLucete(username: str, password: str):
    url = "https://luceteglobal.com/v1/api/users/login"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        COLLECTION_USER = DB_MONGO["user"]
        passWord = Authen.get_password_hash(password)
        userData = {
            "username": username,
            "name": json_data["data"]["name"],
            "password": passWord,
        }
        token = Authen.generate_token(
            name=json_data["data"]["name"],
        )
        COLLECTION_USER.insert_one(userData)
        return json_data["data"]["name"],token
    else:
        return None
