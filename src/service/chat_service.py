from src.agent.agent import Agent
from src.utils.mongodb_utils import DB_MONGO
import json

def chat_bot(
    unit: int,
    prompt: str
):
    agent = Agent("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")
    try:
        if unit:
            url = get_book_url(unit)
            agent.ingest(url)
            answer = agent.ask(prompt)
    except Exception as e:
        return e
        
    return answer

def get_book():
    dict = {}
    COLLECTION_BOOK = DB_MONGO["book"]
    data = list(COLLECTION_BOOK.find({}))
    result = []
    for doc in data:
        dict["title"] = doc.get("title")
        dict["unit_id"] = doc.get("unit_id")
        result.append(dict)
    return result


def get_book_url(
    id: int
):
    try:
        COLLECTION_BOOK = DB_MONGO["book"]
        data = COLLECTION_BOOK.find_one(
            {"unit_id": id}
        )
        return data.get("url")
    except Exception as e:
        print(e)


