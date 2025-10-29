import json
from .alpha_vantage_common import _make_api_request, format_datetime_for_api


def get_news(ticker, start_date, end_date) -> dict[str, str] | str:
    """Returns live and historical market news & sentiment data from premier news outlets worldwide.

    Covers stocks, cryptocurrencies, forex, and topics like fiscal policy, mergers & acquisitions, IPOs.

    Args:
        ticker: Stock symbol for news articles.
        start_date: Start date for news search in yyyy-mm-dd format.
        end_date: End date for news search in yyyy-mm-dd format.

    Returns:
        Dictionary containing news sentiment data or JSON string.

    Raises:
        ValueError: When API returns invalid inputs error (e.g., ticker not supported)
    """
    params = {
        "tickers": ticker,
        "time_from": format_datetime_for_api(start_date),
        "time_to": format_datetime_for_api(end_date),
        "sort": "LATEST",
        "limit": "50",
    }

    result = _make_api_request("NEWS_SENTIMENT", params)

    # Check if the result is an error response and raise exception to trigger fallback
    if isinstance(result, str):
        try:
            result_json = json.loads(result)
            if "Information" in result_json:
                error_msg = result_json["Information"]
                if "Invalid inputs" in error_msg:
                    raise ValueError(
                        f"Alpha Vantage News API does not support ticker '{ticker}'. "
                        "This may be an ETF or unsupported symbol."
                    )
        except json.JSONDecodeError:
            pass  # Not JSON, return as-is

    return result

def get_insider_transactions(symbol: str) -> dict[str, str] | str:
    """Returns latest and historical insider transactions by key stakeholders.

    Covers transactions by founders, executives, board members, etc.

    Args:
        symbol: Ticker symbol. Example: "IBM".

    Returns:
        Dictionary containing insider transaction data or JSON string.
    """

    params = {
        "symbol": symbol,
    }

    return _make_api_request("INSIDER_TRANSACTIONS", params)