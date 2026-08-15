import sqlite3
import logging

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
)
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
)
"""

def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    """Initialize tables."""
    try:
        with _conn() as c:
            c.execute(_CREATE_NEWS_TABLE)
            c.execute(_CREATE_HISTORY_TABLE)
            c.execute("CREATE INDEX IF NOT EXISTS idx_news_comp ON news (comp)")
    except Exception as exc:
        logger.error("DB init failed: %s", exc)