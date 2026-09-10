import logging
import database
from fastapi import FastAPI

app = FastAPI()
database.init_db()

@app.get("/")
def root():
    return {"Hello": "world"}

@app.get("/fuck")
def fuck():
    return {"genuinely": "what"}



# import logging
# from database import init_db, get_recent_news, get_recent_history, _conn
# from fetcher import fetch_and_store_company_data
# from strategy import run_strategy

# logging.basicConfig(level=logging.INFO)

# def run_integration_test(ticker: str = "AAPL"):
#     print(f"\n=== 1. INITIALIZING DATABASE ===")
#     init_db(initial_cash=10000.00)
    
#     print(f"\n=== 2. FETCHING & ANALYZING NEWS FOR {ticker} ===")
#     fetch_and_store_company_data(ticker)
    
#     news = get_recent_news(ticker, limit=5)
#     print(f"Fetched {len(news)} news articles.")
#     if news:
#         print(f"Sample Article Title: {news[0]['title']}")
#         print(f"Sample Title Sentiment: {news[0]['sentiment_title']}")

#     print(f"\n=== 3. RUNNING STRATEGY FOR {ticker} ===")
#     run_strategy(ticker)
    
#     history = get_recent_history(ticker, limit=1)
#     if history:
#         print(f"Latest Analysis: {history[0]}")

#     print(f"\n=== 4. CHECKING DATABASE STATES ===")
#     with _conn() as conn:
#         cash = conn.execute("SELECT * FROM account_state ORDER BY id DESC LIMIT 1").fetchone()
#         portfolio = conn.execute("SELECT * FROM portfolio").fetchall()
#         trades = conn.execute("SELECT * FROM trades").fetchall()

#         print(f"Current Cash Balance: ${cash['cash_balance'] if cash else 'N/A'}")
#         print(f"Portfolio Positions: {[dict(p) for p in portfolio]}")
#         print(f"Executed Trades Count: {len(trades)}")
#         if trades:
#             print(f"Latest Trade: {dict(trades[-1])}")

# if __name__ == "__main__":
#     run_integration_test("AAPL")