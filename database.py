import sqlite3
import logging
from datetime import datetime, timezone

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

def get_recent_news(comp: str, limit: int = 10):
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