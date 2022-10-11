import uvicorn as uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {"status": "Working"}
