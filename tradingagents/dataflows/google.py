from typing import Annotated
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .googlenews_utils import getNewsData


def _enhance_ticker_query(ticker: str) -> str:
    """
    Enhance ticker symbol with financial context to avoid ambiguous search results.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Enhanced query string with financial context
    """
    # Dictionary of commonly confused tickers and their enhancements
    AMBIGUOUS_TICKERS = {
        # ETFs
        "SPY": "SPY ETF S&P 500",
        "QQQ": "QQQ ETF NASDAQ",
        "IWM": "IWM ETF Russell",
        "DIA": "DIA ETF Dow Jones",
        "EEM": "EEM ETF emerging markets",
        "GLD": "GLD ETF gold",
        "TLT": "TLT ETF treasury",
        "VTI": "VTI ETF Vanguard",

        # Stocks with common English words
        "CAT": "CAT stock Caterpillar",
        "COST": "COST stock Costco",
        "DIS": "DIS stock Disney",
        "LOW": "LOW stock Lowe's",
        "NOW": "NOW stock ServiceNow",
        "ALL": "ALL stock Allstate",
        "FAST": "FAST stock Fastenal",
        "NICE": "NICE stock",
        "WELL": "WELL stock Welltower",
        "SAVE": "SAVE stock Spirit Airlines",
    }

    ticker_upper = ticker.upper().strip()

    # If ticker is in the ambiguous list, use enhanced query
    if ticker_upper in AMBIGUOUS_TICKERS:
        return AMBIGUOUS_TICKERS[ticker_upper].replace(" ", "+")

    # For other tickers, check if they're likely ETFs (3-4 letter all caps) or stocks
    # Most ETFs are 3-4 characters, stocks are typically 1-5 characters
    if len(ticker_upper) <= 4 and ticker_upper.isalpha():
        # Add "stock" to avoid confusion with common words
        return f"{ticker}+stock".replace(" ", "+")

    # Return ticker as-is for other cases
    return ticker.replace(" ", "+")


def get_google_news(
    ticker: Annotated[str, "Ticker symbol or query"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve Google News for a given ticker symbol within a date range.

    Args:
        ticker: Ticker symbol or search query
        start_date: Start date in yyyy-mm-dd format
        end_date: End date in yyyy-mm-dd format

    Returns:
        Formatted string containing news articles
    """
    # Add financial context for ambiguous ticker symbols
    query = _enhance_ticker_query(ticker)

    # Parse dates
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Fetch news data
    news_results = getNewsData(query, start_date, end_date)

    # Format results
    if len(news_results) == 0:
        return ""

    news_str = ""
    for news in news_results:
        news_str += (
            f"### {news['title']} (source: {news['source']}) \n\n{news['snippet']}\n\n"
        )

    return f"## {query} Google News, from {start_date} to {end_date}:\n\n{news_str}"