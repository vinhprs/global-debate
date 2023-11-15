from src.agent.agent import Agent
from src.utils.mongodb_utils import DB_MONGO
import os

def chat_bot(
    prompt: str,
    topic_id: int,
    unit_id: int
):
    agent = Agent("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")
    COLLECTION_TOPIC = DB_MONGO["topic"]
    COLLECTION_UNIT = DB_MONGO["book"]
    try:
        if unit_id:
            agent.forget()
            url = get_book_url(unit_id)
            agent.ingest(url)
        topic = COLLECTION_TOPIC.find_one(
            {"topic_id": topic_id}
        )
        unit = COLLECTION_UNIT.find_one(
            {"unit_id": unit_id}
        )
        answer = agent.ask(topic.get("topic_name"), unit.get("title"), prompt)
        print(answer)
    except Exception as e:
        return e
        
    return answer

# def ingest_data(
#     unit_id: int
# ):
#     try:
#         if unit_id:
#             agent.forget()
#             url = get_book_url(unit_id)
#             agent.ingest(url)
#             return True
#     except Exception as e:
#         print(e)
#         return False

def get_topic():
    COLLECTION_TOPIC = DB_MONGO["topic"]
    pipeline = [
        {
            "$lookup": {
                "from": "book",
                "localField": "include_units",
                "foreignField": "unit_id",
                "as": "book"
            }
        },
        {
            "$project": {
                "_id": 0,
                "topic_name": 1,
                "topic_id": 1,
                "book": {
                    "unit_id": 1,
                    "title": 1,
                }
            }
        }
    ]

    result = list(COLLECTION_TOPIC.aggregate(pipeline))
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


