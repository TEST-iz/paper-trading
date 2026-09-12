import logging
import database
from contextlib import asynccontextmanager
from fastapi import FastAPI
import strategy
import fetcher

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database.init_db()
#     yield

app = FastAPI()

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

#should be post for the following three
@app.get("/fetch_news/{comp}")
def fetch_news(comp: str):
    fetcher.fetch_and_store_company_data(comp.upper())
    return {"Finished": "yeah"}

#testing
@app.get("/trade/{comp}")
def trade(comp: str):
    database.execute_paper_trade(comp.upper(), "BUY", 10000, 1000.0)
    return {"Finished": "yeah"}

@app.get("/trade_history")
def get_trades():
    return database.get_recent_trades()