import os
from fastapi import FastAPI
from dotenv import load_dotenv
from base.base import database
from routers import user

load_dotenv("../.env")

app = FastAPI()

app.include_router(user.router)


@app.get('/')
def index():
    return {"status": "Working"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.environ["APP_HOST"], port=os.environ["APP_PORT"])
