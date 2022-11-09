import redis
from dotenv import load_dotenv
import os

from base.schemas import UserDisplayWithId

load_dotenv()


def set_redis(key: int, val: str, current_user: UserDisplayWithId):
    redis_db = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=current_user.id)
    redis_db.set(key, val)
    return print(f'Key: {key}, Value: {val}')
