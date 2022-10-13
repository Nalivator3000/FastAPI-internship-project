import aioredis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')


async def main():
    redis = aioredis.from_url("redis://REDIS_HOST")
    await redis.set("my-key", "value")
    value = await redis.get("my-key")
