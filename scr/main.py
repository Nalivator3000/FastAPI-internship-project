from fastapi import FastAPI
from meduzzen.dbs.database import db

app = FastAPI()


@app.get('/')
def index():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
