import logging
import database
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    yield

app = FastAPI(lifespan=lifespan)

#testing
@app.get("/")
def root():
    return {"Hello": "world"}

@app.get("/fuck")
def fuck():
    return {"genuinely": "what"}