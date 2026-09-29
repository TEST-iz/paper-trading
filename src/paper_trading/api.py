import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from . import database, fetcher, strategy
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database.init_db()
#     yield

class Company(BaseModel):
    comp: str


app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "https://localhost",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#testing
@app.get("/")
def root():
    return {"Hello": "world"}

@app.get("/news/{comp}")
def get_news(comp: str):
    return database.get_recent_news(comp.upper(), 10)

@app.get("/account")
def get_account():
    return database.get_account_state()

@app.get("/history/{comp}")
def get_history(comp: str):
    return database.get_recent_history(comp.upper())

@app.get("/portfolio")
def get_portfolio():
    return database.get_portfolio()

@app.post("/fetch_news")
def fetch_news(company: Company):
    fetcher.fetch_and_store_company_data(company.comp.upper())
    return company

@app.post("/trade")
def trade(company: Company):
    database.execute_paper_trade(company.comp.upper(), "BUY", 10000, 1000.0)
    return {"Finished": "yeah"}

@app.get("/trade_history")
def get_trades():
    return database.get_recent_trades()