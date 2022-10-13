from databases import Database
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_BD_NAME = os.getenv('POSTGRES_DB_NAME')

REDIS_HOST = os.getenv('REDIS_HOST')

app = FastAPI()

db = Database('postgresql+psycopg2://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST/POSTGRES_DB_NAME')


@app.get('/')
def index():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
