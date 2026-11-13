import logging
from datetime import datetime, timezone
import feedparser
import yfinance as yf
from transformers import pipeline
from src.paper_trading.database import save_news_items
import re
import html

logger = logging.getLogger(__name__)

_finbert_pipeline = None

def clean_html(raw_text: str) -> str:
    if not raw_text:
        return ""
    clean_text = re.sub(r'<[^>]*?>', '', raw_text)
    return html.unescape(clean_text).strip()

def get_finbert():
    """Lazily load and return the FinBERT pipeline instance."""
    global _finbert_pipeline
    if _finbert_pipeline is None:
        logger.info("Loading FinBERT model into memory...")
        _finbert_pipeline = pipeline("text-classification", model="ProsusAI/finbert")
    return _finbert_pipeline

def get_finbert_score(content: str):
    if not content:
        return 0.0

    finbert = get_finbert()
    try:
        result = finbert(content[:512])[0]
        label = result["label"].lower()
        score = result["score"]

        if label == "positive":
            return score
        elif label == "negative":
            return -score
        else:
            return 0.0
    except Exception as exc:
        logger.warning("FinBERT scoring failed: %s", exc)
        return 0.0

def fetch_and_store_company_data(comp: str):
    """
    Fetches news articles for a company using Google News RSS,
    runs FinBERT sentiment analysis on title and summary, and stores them in SQLite.
    """
    # Construct a clean Google News RSS query for the ticker over the last day
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={comp.upper()}&region=US&lang=en-US"
    feed = feedparser.parse(url)

    if not feed.entries:
        logger.warning("No RSS news entries returned for %s", comp)
        return False

    articles_to_save = []
    for entry in feed.entries:
        title = entry.get("title", "")
        raw_summary = entry.get("summary", "")
        summary = clean_html(raw_summary)
        guid = entry.get("id") or entry.get("link")
        link = entry.get("link", "")
        pub_date = entry.get("published", datetime.now(timezone.utc).isoformat())

        # Run through FinBERT sentiment analysis
        sent_title = get_finbert_score(title)
        sent_summary = get_finbert_score(summary)

        articles_to_save.append({
            "guid": guid,
            "comp": comp.upper(),
            "title": title,
            "summary": summary,
            "url": link,
            "pub_date": pub_date,
            "sentiment_title": sent_title,
            "sentiment_summary": sent_summary
        })

    save_news_items(articles_to_save)
    logger.info("Saved %d articles for %s using RSS feed & FinBERT", len(articles_to_save), comp)
    return True