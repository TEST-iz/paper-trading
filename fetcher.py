import sqlite3
import pandas as pd
import logging
import yfinance as yf
from datetime import datetime
from transformers import pipeline
from database import init_db, save_news_items

logger = logging.getLogger(__name__)

print("Loading FinBERT model (this may take a moment on first run)...")
finbert = pipeline("text-classification", model="ProsusAI/finbert")

def get_finbert_score(content: str):
    if not content:
        return 0.0

    result = finbert(content[:512])[0]
    label = result["label"].lower()
    score = result["score"]

    if label == "positive":
        return score
    elif label == "negative":
        return -score
    else:
        return 0.0

def fetch_and_store_company_data(comp: str):
    ticker = yf.Ticker(comp)

    ticker_news = ticker.news
    if not ticker_news:
        logger.warning("No news returned for %s", comp)
        return

    articles_to_save = []
    for item in ticker_news:

        content = item.get("content") or item
        title = content.get("title", "")
        summary = content.get("summary", "")

        sent_title = get_finbert_score(title)
        sent_summary = get_finbert_score(summary)

        articles_to_save.append({
            "guid": item.get("id"),
            "comp": comp.upper(),
            "title": title,
            "summary": summary,
            "url": content.get("canonicalUrl", {}).get("url", ""),
            "pub_date": content.get("pubDate"),
            "sentiment_title": sent_title,
            "sentiment_summary": sent_summary
        })
    save_news_items(articles_to_save)
    logger.info("Saved %d articles for %s using Finbert", len(articles_to_save), comp)

