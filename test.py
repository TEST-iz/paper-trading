import sqlite3
import logging
import datetime, timezone

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
            pub_str = pub.isoformat() if isinstance(pub, datetime) else str(pub)
            data.append((
                a['guid'],
                a['comp'],
                a['title'],
                a['summary'],
                a['url'],
                pub_str,
                a.get('sentiment_title'),
                a.get('sentiment_summary')
            ))
        with _conn() as c:
            c.executemany(sql, data)
    except Exception as exc:
        logger.warning("Failed to bulk save news: %s", exc)