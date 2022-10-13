from databases import Database
from fastapi import FastAPI

app = FastAPI()

db = Database('postgresql+psycopg2://postgres:root@localhost/postgres_db')


@app.get('/')
def index():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
