from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_news
from tradingagents.dataflows.config import get_config


def create_social_media_analyst(llm):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_news,
        ]

        system_message = (
            """You are a company-specific news and sentiment analyst tasked with analyzing recent company news and public discussions for a specific company over the past week.

**IMPORTANT LIMITATIONS:**
- You currently have LIMITED access to social media data
- You can only use news articles as a proxy for public sentiment
- Focus on analyzing company-specific news, press releases, and media coverage

**Your Objective:**
Write a comprehensive report covering:
1. Recent company-specific news and announcements
2. Media coverage tone and sentiment (positive, negative, neutral)
3. Key themes and topics in recent discussions
4. Potential implications for traders and investors

**Search Strategy:**
- Use get_news(query, start_date, end_date) with company name and ticker
- Search for "[Company Name] news", "[Ticker] stock news"
- Look for earnings, product launches, management changes, partnerships, etc.

**IMPORTANT - For ticker symbols like SPY, QQQ, etc.:**
- Add financial context (e.g., "SPY ETF", "QQQ stock") to avoid irrelevant results
- Filter out non-financial news

Do not simply state the trends are mixed. Provide detailed and fine-grained analysis based on available news data."""
            + """ Make sure to append a Markdown table at the end of the report to organize key points in the report, organized and easy to read.""",
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
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
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

        return {
            "messages": [result],
            "sentiment_report": report,
        }

    return social_media_analyst_node
