import os
import certifi
from pymongo import MongoClient

def get_database(dbname: str) -> str:
    CONNECTION_STRING = "mongodb+srv://vinhprs:19052002@cluster0.znnks5j.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[dbname]


DB_MONGO = get_database(dbname="wing_test")
