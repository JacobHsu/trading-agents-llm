import questionary
import os
from typing import List, Optional, Tuple, Dict
from rich.console import Console

from cli.models import AnalystType
from cli.i18n import i18n

console = Console()

ANALYST_ORDER = [
    ("Market Analyst", AnalystType.MARKET),
    ("Social Media Analyst", AnalystType.SOCIAL),
    ("News Analyst", AnalystType.NEWS),
    ("Fundamentals Analyst", AnalystType.FUNDAMENTALS),
]


def get_ticker() -> str:
    """Prompt the user to enter a ticker symbol."""
    ticker = questionary.text(
        i18n("step_1_prompt") + ":",
        validate=lambda x: len(x.strip()) > 0 or i18n("invalid_ticker"),
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not ticker:
        console.print(f"\n[red]{i18n('no_ticker_provided')}[/red]")
        exit(1)

    return ticker.strip().upper()


def get_analysis_date() -> str:
    """Prompt the user to enter a date in YYYY-MM-DD format."""
    import re
    from datetime import datetime, timedelta

    def validate_date(date_str: str) -> bool:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # 計算前一個交易日（避開週末）
    today = datetime.now()
    days_back = 1
    # 如果今天是週一，前一個交易日是週五（回退3天）
    if today.weekday() == 0:  # Monday
        days_back = 3
    # 如果今天是週日，前一個交易日是週五（回退2天）
    elif today.weekday() == 6:  # Sunday
        days_back = 2

    default_date = (today - timedelta(days=days_back)).strftime("%Y-%m-%d")

    date = questionary.text(
        i18n("step_2_prompt") + " (YYYY-MM-DD):",
        default=default_date,
        validate=lambda x: validate_date(x.strip())
        or i18n("invalid_date_format"),
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not date:
        console.print(f"\n[red]{i18n('no_date_provided')}[/red]")
        exit(1)

    return date.strip()


def select_analysts() -> List[AnalystType]:
    """Select analysts using an interactive checkbox."""
    choices = questionary.checkbox(
        i18n("select_analysts_team"),
        choices=[
            questionary.Choice(display, value=value, checked=(value == AnalystType.MARKET))
            for display, value in ANALYST_ORDER
        ],
        instruction=f"\n{i18n('space_to_select')}\n{i18n('a_to_select_all')}\n{i18n('enter_when_done')}",
        validate=lambda x: len(x) > 0 or i18n("must_select_one_analyst"),
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        console.print(f"\n[red]{i18n('no_analysts_selected')}[/red]")
        exit(1)

    return choices


def select_research_depth() -> int:
    """Select research depth using an interactive selection."""

    # Define research depth options with their corresponding values
    DEPTH_OPTIONS = [
        (i18n("shallow_research"), 1),
        (i18n("medium_research"), 3),
        (i18n("deep_research"), 5),
    ]

    choice = questionary.select(
        i18n("select_research_depth"),
        choices=[
            questionary.Choice(display, value=value) for display, value in DEPTH_OPTIONS
        ],
        instruction=f"\n{i18n('use_arrow_keys')}\n{i18n('press_enter_to_select')}",
        style=questionary.Style(
            [
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(f"\n[red]{i18n('no_research_depth_selected')}[/red]")
        exit(1)

    return choice


def select_shallow_thinking_agent(provider) -> str:
    """Select shallow thinking llm engine using an interactive selection."""

    # Define shallow thinking llm engine options with their corresponding model names
    # 根據當前語言選擇選項描述
    lang = os.environ.get("TRADINGAGENTS_LANG", "zh_TW")

    if lang == "zh_TW":
        SHALLOW_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4o-mini - 快速高效的任務處理", "gpt-4o-mini"),
                ("GPT-4.1-nano - 超輕量級基礎操作模型", "gpt-4.1-nano"),
                ("GPT-4.1-mini - 緊湊型高性能模型", "gpt-4.1-mini"),
                ("GPT-4o - 標準可靠能力模型", "gpt-4o"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - 快速推理與標準能力", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - 高能力標準模型", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - 卓越混合推理與智能體能力", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - 高性能與優秀推理", "claude-sonnet-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - 成本效益與低延遲", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - 次世代功能、速度與思考", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - 自適應思考、成本效益", "gemini-2.5-flash-preview-05-20"),
            ],
            "openrouter": [
                ("Meta: Llama 4 Scout", "meta-llama/llama-4-scout:free"),
                ("Meta: Llama 3.3 8B Instruct - Llama 3.3 70B 的輕量級超快變體", "meta-llama/llama-3.3-8b-instruct:free"),
                ("google/gemini-2.0-flash-exp:free - Gemini Flash 2.0 顯著更快的首令牌時間", "google/gemini-2.0-flash-exp:free"),
            ],
            "ollama": [
                ("llama3.1 本地", "llama3.1"),
                ("llama3.2 本地", "llama3.2"),
            ]
        }
    elif lang == "zh_CN":
        SHALLOW_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4o-mini - 快速高效的任务处理", "gpt-4o-mini"),
                ("GPT-4.1-nano - 超轻量级基础操作模型", "gpt-4.1-nano"),
                ("GPT-4.1-mini - 紧凑型高性能模型", "gpt-4.1-mini"),
                ("GPT-4o - 标准可靠能力模型", "gpt-4o"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - 快速推理与标准能力", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - 高能力标准模型", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - 卓越混合推理与智能体能力", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - 高性能与优秀推理", "claude-sonnet-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - 成本效益与低延迟", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - 次世代功能、速度与思考", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - 自适应思考、成本效益", "gemini-2.5-flash-preview-05-20"),
            ],
            "openrouter": [
                ("Meta: Llama 4 Scout", "meta-llama/llama-4-scout:free"),
                ("Meta: Llama 3.3 8B Instruct - Llama 3.3 70B 的轻量级超快变体", "meta-llama/llama-3.3-8b-instruct:free"),
                ("google/gemini-2.0-flash-exp:free - Gemini Flash 2.0 显著更快的首令牌时间", "google/gemini-2.0-flash-exp:free"),
            ],
            "ollama": [
                ("llama3.1 本地", "llama3.1"),
                ("llama3.2 本地", "llama3.2"),
            ]
        }
    else:  # en_US
        SHALLOW_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4o-mini - Fast and efficient for quick tasks", "gpt-4o-mini"),
                ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
                ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
                ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
            ],
            "openrouter": [
                ("Meta: Llama 4 Scout", "meta-llama/llama-4-scout:free"),
                ("Meta: Llama 3.3 8B Instruct - A lightweight and ultra-fast variant of Llama 3.3 70B", "meta-llama/llama-3.3-8b-instruct:free"),
                ("google/gemini-2.0-flash-exp:free - Gemini Flash 2.0 offers a significantly faster time to first token", "google/gemini-2.0-flash-exp:free"),
            ],
            "ollama": [
                ("llama3.1 local", "llama3.1"),
                ("llama3.2 local", "llama3.2"),
            ]
        }

    # 設定預設選項（根據 provider）
    default_shallow = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-latest",
        "google": "gemini-2.0-flash",
        "openrouter": "meta-llama/llama-4-scout:free",
        "ollama": "llama3.2"
    }

    choice = questionary.select(
        i18n("select_quick_thinking_llm"),
        choices=[
            questionary.Choice(display, value=value)
            for display, value in SHALLOW_AGENT_OPTIONS[provider.lower()]
        ],
        default=default_shallow.get(provider.lower()),
        instruction=f"\n{i18n('use_arrow_keys')}\n{i18n('press_enter_to_select')}",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(
            f"\n[red]{i18n('no_shallow_thinking_selected')}[/red]"
        )
        exit(1)

    return choice


def select_deep_thinking_agent(provider) -> str:
    """Select deep thinking llm engine using an interactive selection."""

    # Define deep thinking llm engine options with their corresponding model names
    # 根據當前語言選擇選項描述
    lang = os.environ.get("TRADINGAGENTS_LANG", "zh_TW")

    if lang == "zh_TW":
        DEEP_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4.1-nano - 超輕量級基礎操作模型", "gpt-4.1-nano"),
                ("GPT-4.1-mini - 緊湊型高性能模型", "gpt-4.1-mini"),
                ("GPT-4o - 標準可靠能力模型", "gpt-4o"),
                ("o4-mini - 專業推理模型（緊湊型）", "o4-mini"),
                ("o3-mini - 進階推理模型（輕量級）", "o3-mini"),
                ("o3 - 完整進階推理模型", "o3"),
                ("o1 - 頂級推理與問題解決模型", "o1"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - 快速推理與標準能力", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - 高能力標準模型", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - 卓越混合推理與智能體能力", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - 高性能與優秀推理", "claude-sonnet-4-0"),
                ("Claude Opus 4 - Anthropic 最強大模型", "claude-opus-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - 成本效益與低延遲", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - 次世代功能、速度與思考", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - 自適應思考、成本效益", "gemini-2.5-flash-preview-05-20"),
                ("Gemini 2.5 Pro", "gemini-2.5-pro-preview-06-05"),
            ],
            "openrouter": [
                ("DeepSeek V3 - 685B 參數混合專家模型", "deepseek/deepseek-chat-v3-0324:free"),
                ("Deepseek - DeepSeek 團隊旗艦對話模型最新版本", "deepseek/deepseek-chat-v3-0324:free"),
            ],
            "ollama": [
                ("llama3.1 本地", "llama3.1"),
                ("qwen3", "qwen3"),
            ]
        }
    elif lang == "zh_CN":
        DEEP_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4.1-nano - 超轻量级基础操作模型", "gpt-4.1-nano"),
                ("GPT-4.1-mini - 紧凑型高性能模型", "gpt-4.1-mini"),
                ("GPT-4o - 标准可靠能力模型", "gpt-4o"),
                ("o4-mini - 专业推理模型（紧凑型）", "o4-mini"),
                ("o3-mini - 进阶推理模型（轻量级）", "o3-mini"),
                ("o3 - 完整进阶推理模型", "o3"),
                ("o1 - 顶级推理与问题解决模型", "o1"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - 快速推理与标准能力", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - 高能力标准模型", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - 卓越混合推理与智能体能力", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - 高性能与优秀推理", "claude-sonnet-4-0"),
                ("Claude Opus 4 - Anthropic 最强大模型", "claude-opus-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - 成本效益与低延迟", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - 次世代功能、速度与思考", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - 自适应思考、成本效益", "gemini-2.5-flash-preview-05-20"),
                ("Gemini 2.5 Pro", "gemini-2.5-pro-preview-06-05"),
            ],
            "openrouter": [
                ("DeepSeek V3 - 685B 参数混合专家模型", "deepseek/deepseek-chat-v3-0324:free"),
                ("Deepseek - DeepSeek 团队旗舰对话模型最新版本", "deepseek/deepseek-chat-v3-0324:free"),
            ],
            "ollama": [
                ("llama3.1 本地", "llama3.1"),
                ("qwen3", "qwen3"),
            ]
        }
    else:  # en_US
        DEEP_AGENT_OPTIONS = {
            "openai": [
                ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
                ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
                ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
                ("o4-mini - Specialized reasoning model (compact)", "o4-mini"),
                ("o3-mini - Advanced reasoning model (lightweight)", "o3-mini"),
                ("o3 - Full advanced reasoning model", "o3"),
                ("o1 - Premier reasoning and problem-solving model", "o1"),
            ],
            "anthropic": [
                ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
                ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
                ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
                ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
                ("Claude Opus 4 - Most powerful Anthropic model", "claude-opus-4-0"),
            ],
            "google": [
                ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
                ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
                ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
                ("Gemini 2.5 Pro", "gemini-2.5-pro-preview-06-05"),
            ],
            "openrouter": [
                ("DeepSeek V3 - a 685B-parameter, mixture-of-experts model", "deepseek/deepseek-chat-v3-0324:free"),
                ("Deepseek - latest iteration of the flagship chat model family from the DeepSeek team.", "deepseek/deepseek-chat-v3-0324:free"),
            ],
            "ollama": [
                ("llama3.1 local", "llama3.1"),
                ("qwen3", "qwen3"),
            ]
        }
    
    # 設定預設選項（根據 provider）
    default_deep = {
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-latest",
        "google": "gemini-2.5-flash-preview-05-20",
        "openrouter": "deepseek/deepseek-chat-v3-0324:free",
        "ollama": "llama3.1"
    }

    choice = questionary.select(
        i18n("select_deep_thinking_llm"),
        choices=[
            questionary.Choice(display, value=value)
            for display, value in DEEP_AGENT_OPTIONS[provider.lower()]
        ],
        default=default_deep.get(provider.lower()),
        instruction=f"\n{i18n('use_arrow_keys')}\n{i18n('press_enter_to_select')}",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(f"\n[red]{i18n('no_deep_thinking_selected')}[/red]")
        exit(1)

    return choice

def select_llm_provider() -> tuple[str, str]:
    """Select the OpenAI api url using interactive selection."""
    # Define OpenAI api options with their corresponding endpoints
    BASE_URLS = [
        ("OpenAI", "https://api.openai.com/v1"),
        ("Anthropic", "https://api.anthropic.com/"),
        ("Google", "https://generativelanguage.googleapis.com/v1"),
        ("Openrouter", "https://openrouter.ai/api/v1"),
        ("Ollama", "http://localhost:11434/v1"),        
    ]
    
    choice = questionary.select(
        i18n("select_llm_provider"),
        choices=[
            questionary.Choice(display, value=(display, value))
            for display, value in BASE_URLS
        ],
        default=("Google", "https://generativelanguage.googleapis.com/v1"),
        instruction=f"\n{i18n('use_arrow_keys')}\n{i18n('press_enter_to_select')}",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(f"\n[red]{i18n('no_backend_selected')}[/red]")
        exit(1)

    display_name, url = choice
    print(f"{i18n('you_selected')}: {display_name}\t{i18n('url')}: {url}")

    return display_name, url
