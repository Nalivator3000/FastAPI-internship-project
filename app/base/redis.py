import redis
from dotenv import load_dotenv
import os

from fastapi import HTTPException, status
from redis.client import Redis

load_dotenv()


def set_redis(key: int, val: str):
    try:
        redis_db = get_redis()
        redis_db.set(key, val)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The answer was not recorded")


def get_redis() -> Redis:
    return redis.from_url(os.getenv('REDIS_URL'))
