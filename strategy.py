from database import execute_paper_trade, get_recent_news, save_analysis
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def calculate_combined_sentiment(news_items: list[dict]):
    combined_scores = []

    for item in news_items:
        title_score = item.get("sentiment_title") or 0.0
        summary_score = item.get("sentiment_summary") or 0.0

        article_score = (0.6 * title_score) + (0.4 * summary_score)
        combined_scores.append(article_score)

    return sum(combined_scores) / len(combined_scores) if combined_scores else 0.0

def run_strategy(comp: str):
    news_items = get_recent_news(comp)
    
    if not news_items:
        return

    avg_sentiment = calculate_combined_sentiment(news_items)
    if avg_sentiment > 0.20:
        verdict = "BUY"
        confidence = min((avg_sentiment - 0.2) / (1.0 - 0.2), 1.0)
    elif avg_sentiment < -0.20:
        verdict = "SELL"
        confidence = min((abs(avg_sentiment) - 0.2) / (1.0 - 0.2), 1.0)
    else:
        verdict = "HOLD"
        confidence = 0.50

    save_analysis(
        comp=comp,
        verdict=verdict,
        confidence=confidence,
        sentiment=avg_sentiment,
        count=len(news_items),
    )

    if verdict in ("BUY", "SELL"):
        try:
            ticker = yf.Ticker(comp)
            price = ticker.fast_info.get("lastPrice") or ticker.fast_info.get("previousClose")
            
            if price:
                shares = max(1, int(abs(avg_sentiment) * 10))
                success = execute_paper_trade(comp=comp, action=verdict, shares=shares, price=price)
                if success:
                    print(f"[{verdict}] {comp} @ ${price:.2f} | Sentiment: {avg_sentiment:.2f}")
            else:
                logger.warning("Could not fetch price for %s", comp)
        except Exception as exc:
            logger.error("Failed to execute trade for %s: %s", comp, exc)