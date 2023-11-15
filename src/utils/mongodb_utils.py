import os
import certifi
from pymongo import MongoClient

def get_database(dbname: str) -> str:
    CONNECTION_STRING = "mongodb+srv://vinhprs:19052002@cluster0.znnks5j.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    return client[dbname]


DB_MONGO = get_database(dbname="wing_test")
