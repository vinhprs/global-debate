import os

import redis
from dotenv import load_dotenv

load_dotenv()


def redis_connection() -> redis.Redis:
    return redis.Redis(
        host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"], db=0
    )

caching = redis_connection()

def set_key_redis(key: str, value: str, expire_time: int = None):
    try:
        caching.set(key, value, ex=expire_time)
    except Exception as e:
        print(e)

def get_key_redis(key: str):
    try:
        return caching.get(key)
    except Exception as e:
        print(e)
        return None
