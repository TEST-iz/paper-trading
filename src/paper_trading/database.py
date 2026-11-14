import sqlite3
import logging
from datetime import datetime, timezone
import yfinance as yf

DB_PATH = "stock_data.db"
logger = logging.getLogger(__name__)

# SQL Schema
_CREATE_NEWS_TABLE = """
CREATE TABLE IF NOT EXISTS news (
    guid TEXT PRIMARY KEY,
    comp TEXT NOT NULL,
    title TEXT,
    summary TEXT,
    url TEXT,
    pub_date TEXT,
    sentiment_title REAL,
    sentiment_summary REAL
);
"""

_CREATE_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comp TEXT NOT NULL,
    pub_date TEXT NOT NULL,
    verdict TEXT,
    confidence_score REAL,
    avg_sentiment REAL,
    articles_count INTEGER
);
"""

_CREATE_PORTFOLIO_TABLE = """
CREATE TABLE IF NOT EXISTS portfolio (
    comp TEXT PRIMARY KEY,
    shares INTEGER NOT NULL DEFAULT 0,
    last_price INTEGER,
    updated_at TEXT NOT NULL
);
"""


_CREATE_TRADES_TABLE = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comp TEXT NOT NULL,
    action TEXT CHECK(action IN ('BUY', 'SELL')) NOT NULL,
    shares INTEGER NOT NULL,
    price REAL NOT NULL,
    total_amount REAL NOT NULL,
    timestamp TEXT NOT NULL
);
"""

_CREATE_ACCOUNT_TABLE = """
CREATE TABLE IF NOT EXISTS account_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cash_balance REAL NOT NULL,
    timestamp TEXT NOT NULL
);
"""

_CREATE_SNAPSHOTS_TABLE = """
CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    cash_balance REAL NOT NULL,
    stock_value REAL NOT NULL,
    total_value REAL NOT NULL,
    run_type TEXT NOT NULL CHECK(run_type IN ('MORNING', 'EVENING'))
);
"""

def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL;")
    return c

def init_db(initial_cash: float = 10000.00):
    """Initialize tables."""
    try:
        with _conn() as c:
            c.execute(_CREATE_NEWS_TABLE)
            c.execute(_CREATE_HISTORY_TABLE)
            c.execute(_CREATE_ACCOUNT_TABLE)
            c.execute(_CREATE_PORTFOLIO_TABLE)
            c.execute(_CREATE_TRADES_TABLE)
            c.execute(_CREATE_SNAPSHOTS_TABLE)
            c.execute("CREATE INDEX IF NOT EXISTS idx_news_comp ON news (comp)")

            row = c.execute("SELECT COUNT(*) as count FROM account_state").fetchone()
            if row["count"] == 0:
                ts = datetime.now(timezone.utc).isoformat()
                c.execute(
                    "INSERT INTO account_state (cash_balance, timestamp) VALUES (?, ?)",
                    (initial_cash, ts)
                )
    except Exception as exc:
        logger.error("DB init failed: %s", exc)

def save_news_items(articles: list[dict]):
    """
    Saves a list of articles.
    Uses 'INSERT OR IGNORE' so duplicate GUIDs are silently skipped.
    """
    sql = """
    INSERT OR IGNORE INTO news (
        guid, comp, title, summary, url, pub_date, sentiment_title, sentiment_summary
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    try:
        data = []
        for a in articles:
            pub = a.get('pub_date')
            if isinstance(pub, datetime):
                pub_str = pub.isoformat()
            elif pub is not None:
                pub_str = str(pub)
            else:
                pub_str = None
            data.append((
                a.get('guid'),
                a.get('comp'),
                a.get('title'),
                a.get('summary'),
                a.get('url'),
                pub_str,
                a.get('sentiment_title'),
                a.get('sentiment_summary')
            ))
        with _conn() as c:
            c.executemany(sql, data)
    except Exception as exc:
        logger.warning("Failed to bulk save news: %s", exc)

def save_analysis(comp: str, verdict: str, confidence: float, sentiment: float, count: int):
    """Saves a summary verdict of a single analysis run."""
    sql = """
    INSERT INTO analysis_history (comp, pub_date, verdict, confidence_score, avg_sentiment, articles_count)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    ts = datetime.now(timezone.utc).isoformat()
    try:
        with _conn() as c:
            c.execute(sql, (comp, ts, verdict, confidence, sentiment, count))
    except Exception as exc:
        logger.warning("Failed to save analysis: %s", exc)

def get_analysis(limit: int = 10):
    sql = "SELECT * FROM analysis_history ORDER BY pub_date DESC LIMIT?"
    with _conn() as c:
        rows = c.execute(sql, (limit,)).fetchall()
        return [dict(r) for r in rows]

def get_recent_trades(limit: int = 10):
    sql = "SELECT * FROM trades ORDER BY timestamp DESC LIMIT ?"
    with _conn() as c:
        rows = c.execute(sql, (limit,)).fetchall()
        return [dict(r) for r in rows]

def get_recent_news(limit: int = 10):
    """Fetch news for a ticker to display or analyze."""
    sql = "SELECT * FROM news ORDER BY pub_date DESC LIMIT ?"
    with _conn() as c:
        rows = c.execute(sql, (limit,)).fetchall()
        return [dict(r) for r in rows]
    
def get_recent_news_comp(comp: str, limit: int = 10):
    """Fetch news for a ticker to display or analyze."""
    sql = "SELECT * FROM news WHERE comp = ? ORDER BY pub_date DESC LIMIT ?"
    with _conn() as c:
        rows = c.execute(sql, (comp, limit)).fetchall()
        return [dict(r) for r in rows]

def get_recent_history(comp: str, limit: int = 1):
    sql = "SELECT * FROM analysis_history WHERE comp = ? ORDER BY pub_date DESC LIMIT ?"
    with _conn() as conn:
        rows = conn.execute(sql, (comp, limit)).fetchall()
        return [dict(r) for r in rows]

def get_account_state():
    with _conn() as c:
        return dict(c.execute("SELECT * FROM account_state ORDER BY id DESC LIMIT 1").fetchone())

def get_portfolio():
    with _conn() as c:
        rows = c.execute("SELECT * FROM portfolio WHERE shares > 0").fetchall()
        return [dict(r) for r in rows]
    
def get_current_price(comp: str) -> float:
    """Fetches the latest available stock price using yfinance."""
    try:
        ticker = yf.Ticker(comp.upper())
        price = ticker.fast_info.get("lastPrice") or ticker.fast_info.get("previousClose")
        if price:
            return float(price)
            
        hist = ticker.history(period="1d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception as exc:
        logger.error("Could not fetch price for %s: %s", comp, exc)
    return 0.0


def execute_paper_trade(comp: str, action: str, shares: int, price: float) -> bool:
    ts = datetime.now(timezone.utc).isoformat()
    total_cost = shares * price

    conn = _conn()
    try:
        with conn:
            account = conn.execute(
                "SELECT cash_balance FROM account_state ORDER BY id DESC LIMIT 1"
            ).fetchone()
            
            if not account:
                logger.error("Account state not initialized.")
                return False
                
            cash = account["cash_balance"]

            if action == "BUY":
                if cash < total_cost:
                    logger.warning("Insufficient cash.")
                    return False
                
                new_cash = cash - total_cost
                
                conn.execute(
                    "INSERT INTO trades (comp, action, shares, price, total_amount, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (comp, action, shares, price, total_cost, ts)
                )
                
                curr_pos = conn.execute("SELECT shares FROM portfolio WHERE comp = ?", (comp,)).fetchone()
                if curr_pos:
                    conn.execute("UPDATE portfolio SET shares = ?, last_price = ?, updated_at = ? WHERE comp = ?", (curr_pos["shares"] + shares, price, ts, comp))
                else:
                    conn.execute("INSERT INTO portfolio (comp, shares, last_price, updated_at) VALUES (?, ?, ?, ?)", (comp, shares, price, ts))

            elif action == "SELL":
                curr_pos = conn.execute("SELECT shares FROM portfolio WHERE comp = ?", (comp,)).fetchone()
                if not curr_pos or shares > curr_pos["shares"]:
                    logger.warning("Invalid position/shares for SELL.")
                    return False

                new_cash = cash + total_cost
                new_shares = curr_pos["shares"] - shares

                conn.execute(
                    "INSERT INTO trades (comp, action, shares, price, total_amount, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (comp, action, shares, price, total_cost, ts)
                )

                if new_shares == 0:
                    conn.execute("DELETE FROM portfolio WHERE comp = ?", (comp,))
                else:
                    conn.execute("UPDATE portfolio SET shares = ?, last_price = ?, updated_at = ? WHERE comp = ?", (new_shares, price, ts, comp))

            else:
                return False

            conn.execute("INSERT INTO account_state (cash_balance, timestamp) VALUES (?, ?)", (new_cash, ts))
            return True

    except Exception as exc:
        logger.error("Trade failed and changes were rolled back: %s", exc)
        return False
    finally:
        conn.close()

def record_portfolio_snapshot(run_type: str):
    """Calculates total net worth (Cash + Active Stocks) and saves a snapshot."""
    conn = _conn()
    try:
        with conn:
            # 1. Get latest cash balance
            account = conn.execute("SELECT cash_balance FROM account_state ORDER BY id DESC LIMIT 1").fetchone()
            cash_balance = account["cash_balance"] if account else 0.0

            # 2. Get active stock holdings
            holdings = conn.execute("SELECT comp, shares FROM portfolio WHERE shares > 0").fetchall()
            
            stock_value = 0.0
            for row in holdings:
                price = get_current_price(row["comp"])
                stock_value += row["shares"] * price

            total_value = cash_balance + stock_value
            timestamp = datetime.now(timezone.utc).isoformat()

            # 3. Save to snapshot table
            conn.execute(
                """
                INSERT INTO portfolio_snapshots (timestamp, cash_balance, stock_value, total_value, run_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (timestamp, cash_balance, stock_value, total_value, run_type)
            )
    except Exception as exc:
        logger.error("Failed to record snapshot: %s", exc)
    finally:
        conn.close()