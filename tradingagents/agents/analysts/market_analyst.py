from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators
from tradingagents.dataflows.config import get_config


def create_market_analyst(llm):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_stock_data,
            get_indicators,
        ]

        system_message = (
            """# Technical Analysis Guidelines

## CRITICAL: Data Validation Rules
**BEFORE providing any analysis, you MUST:**
1. Successfully retrieve AT LEAST 3 technical indicators from the following list:
   - rsi (Relative Strength Index)
   - macd, macds, macdh (MACD indicators)
   - boll, boll_ub, boll_lb (Bollinger Bands)
   - close_50_sma, close_200_sma (Simple Moving Averages)
   - close_10_ema (Exponential Moving Average)
   - atr (Average True Range)
2. Verify the data is complete and recent (within the requested date range)
3. If you CANNOT retrieve sufficient indicator data, you MUST:
   - Return an error message starting with "ERROR: DATA_FETCH_FAILED"
   - Explain which indicators failed to load
   - List possible causes (network issue, API problem, invalid date, etc.)
   - DO NOT attempt to provide analysis with incomplete data
   - DO NOT generate a report based only on price data

## Moving Averages
- **close_50_sma, close_200_sma**: Simple Moving Averages tracking medium and long-term trends.
- **close_10_ema**: Exponential Moving Average reacting faster to recent price changes.
- **Bullish Signal**: Price above moving averages, shorter-term MAs above longer-term MAs.
- **Bearish Signal**: Price below moving averages, shorter-term MAs below longer-term MAs.

## Momentum Indicators
- **rsi (Relative Strength Index)**: Measures speed and magnitude of price changes.
  - Above 70: Overbought (potential pullback)
  - Below 30: Oversold (potential bounce)
  - 40-60: Neutral zone

- **macd, macds, macdh (Moving Average Convergence Divergence)**: Shows relationship between two moving averages.
  - macd: The MACD line
  - macds: The signal line
  - macdh: The histogram (difference between macd and macds)
  - MACD line above signal line: Bullish
  - MACD line below signal line: Bearish
  - Histogram crossing zero: Potential trend change

## Volatility Indicators
- **boll, boll_ub, boll_lb (Bollinger Bands)**: Show price volatility and potential reversal points.
  - boll: Middle band (20-period SMA)
  - boll_ub: Upper band (middle + 2 standard deviations)
  - boll_lb: Lower band (middle - 2 standard deviations)
  - Price touching upper band: Potential resistance, possible pullback
  - Price touching lower band: Potential support, possible bounce
  - Bands narrowing: Low volatility, potential breakout
  - Bands widening: High volatility, strong trend

- **atr (Average True Range)**: Measures market volatility.
  - High ATR: Increased volatility, larger price swings
  - Low ATR: Decreased volatility, smaller price movements

## Analysis Framework
When analyzing indicators:
1. Look for confluence (multiple indicators confirming same signal)
2. Consider overall market trend and conditions
3. Note any divergences between price and indicators
4. Assess risk/reward based on volatility measures
5. Provide specific entry/exit levels when possible

Always conclude your analysis with a clear assessment of the current technical picture and potential trading implications."""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

            # 數據驗證：檢查是否有數據獲取失敗
            if "ERROR: DATA_FETCH_FAILED" in report:
                error_msg = (
                    f"\n\n{'='*80}\n"
                    f"❌ 數據獲取失敗 - 無法生成可靠的分析報告\n"
                    f"{'='*80}\n\n"
                    f"{report}\n\n"
                    f"{'='*80}\n"
                    f"排查建議：\n"
                    f"1. 檢查網絡連接是否正常\n"
                    f"2. 確認使用的日期是交易日（不是週末/假日）\n"
                    f"3. 使用前一個交易日的日期（數據更完整）\n"
                    f"4. 檢查 yfinance 服務是否正常\n"
                    f"5. 稍後重試\n"
                    f"{'='*80}\n"
                )
                raise RuntimeError(error_msg)

        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
