import json
import src.middleware.authen as Authen
from src.utils.mongodb_utils import DB_MONGO
import requests


def authen(username: str, password: str):
    # user = get_user()
    COLLECTION_USER = DB_MONGO["user"]
    queryUsername = {"username": username}
    userName = COLLECTION_USER.find_one(queryUsername)

    queryEmail = {"email": username}
    userEmail = COLLECTION_USER.find_one(queryEmail)

    if userName:
        if Authen.verify_password(password, userName["password"]):
            token = Authen.generate_token(mail=userName["email"], name=username)

            return userName["email"], token, userName["username"]
    if userEmail:
        if Authen.verify_password(password, userEmail["password"]):
            token = Authen.generate_token(mail=userEmail["email"], name=username)

            return userEmail["email"], token

    return None


def get_user(username: str):
    COLLECTION_USER = DB_MONGO["user"]
    myquery = {"username": username}
    user_data = COLLECTION_USER.find_one(myquery)
    return user_data


def register(email: str, username: str, password: str):
    COLLECTION_USER = DB_MONGO["user"]

    if COLLECTION_USER.find_one({"$or": [{"username": username}, {"email": email}]}):
        return None

    hashed_password = Authen.get_password_hash(password)
    user_data = {"username": username, "email": email, "password": hashed_password}

    token = Authen.generate_token(mail=email, name=username)
    COLLECTION_USER.insert_one(user_data)

    return email, token, username


def loginLucete(username: str, password: str):
    url = "https://luceteglobal.com/v1/api/users/login"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        json_data = json.loads(response.content)
        COLLECTION_USER = DB_MONGO["user"]
        myqueryUsername = {"username": username}
        user_data = COLLECTION_USER.find_one(myqueryUsername)
        if user_data and user_data["username"] == username:
            token = Authen.generate_token(
                mail=None,
                name=user_data["username"],
            )
            print(user_data)
            return user_data["username"], token

        passWord = Authen.get_password_hash(password)
        userData = {
            "username": username,
            "email": None,
            "password": passWord,
        }
        # print(json_data["data"]["name"],userData)
        token = Authen.generate_token(mail=None, name=json_data["data"]["name"])
        COLLECTION_USER.insert_one(userData)

        return json_data["data"]["name"], token
    else:
        return None
