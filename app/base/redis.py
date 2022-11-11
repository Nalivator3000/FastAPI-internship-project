import redis
from dotenv import load_dotenv
import os

from fastapi import HTTPException, status
from redis.client import Redis

load_dotenv()


def set_redis(key: str, val: str):
    try:
        redis_db = redis_url()
        redis_db.setex(key, int(os.getenv('REDIS_EXP')), val)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The answer was not recorded")


def get_redis(key: str):
    try:
        redis_db = redis_url()
        return redis_db.get(key)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The answer was not recorded")


def mset_redis(dict_data: dict):
    try:
        redis_db = redis_url()
        redis_db.mset(dict_data)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The answer was not recorded")


def mget_redis(quiz_result: dict):
    try:
        redis_db = redis_url()
        return redis_db.mget(quiz_result)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The answer was not recorded")


def find_records(quiz_id: int, user_id: int = None):
    redis_db = redis_url()
    records = []
    if user_id is not None:
        for record in redis_db.scan_iter(match=f'{quiz_id}--{user_id}--*'):
            record = str(record)
            record = record[2:-1]
            answer = str(get_redis(record))
            full_record = f'{record}--{answer[2:-1]}'
            records.append(full_record)
    else:
        for record in redis_db.scan_iter(match=f'{quiz_id}--*'):
            record = str(record)
            record = record[2:-1]
            answer = str(get_redis(record))
            full_record = f'{record}--{answer[2:-1]}'
            records.append(full_record)
    print(records)
    return records


def redis_url() -> Redis:
    return redis.from_url(os.getenv('REDIS_URL'))
