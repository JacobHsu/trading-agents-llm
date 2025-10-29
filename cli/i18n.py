"""
TradingAgents CLI 國際化支援
支援語言：繁體中文 (zh_TW)、簡體中文 (zh_CN)、英文 (en_US)
"""

import os

# 翻譯字典
TRANSLATIONS = {
    "zh_TW": {
        # 歡迎訊息
        "welcome_title": "歡迎使用 TradingAgents",
        "welcome_subtitle": "多智能體 LLM 金融交易框架",
        "welcome_header": "TradingAgents：多智能體 LLM 金融交易框架 - CLI",
        "welcome_workflow": "工作流程步驟：",
        "welcome_workflow_steps": "I. 分析師團隊 → II. 研究團隊 → III. 交易員 → IV. 風險管理 → V. 投資組合管理",
        "built_by": "由 Tauric Research 建構",

        # 步驟標題
        "step_1_title": "步驟 1：股票代碼",
        "step_1_prompt": "輸入要分析的股票代碼",
        "step_2_title": "步驟 2：分析日期",
        "step_2_prompt": "輸入分析日期 (YYYY-MM-DD)",
        "step_3_title": "步驟 3：分析師團隊",
        "step_3_prompt": "選擇您的 LLM 分析師智能體進行分析",
        "step_4_title": "步驟 4：研究深度",
        "step_4_prompt": "選擇您的研究深度層級",
        "step_5_title": "步驟 5：OpenAI 後端",
        "step_5_prompt": "選擇要使用的服務",
        "step_6_title": "步驟 6：思考智能體",
        "step_6_prompt": "選擇您的思考智能體進行分析",

        # 分析師類型
        "market_analyst": "市場分析師",
        "social_analyst": "社交媒體分析師",
        "news_analyst": "新聞分析師",
        "fundamentals_analyst": "基本面分析師",

        # 研究團隊
        "bull_researcher": "看漲研究員",
        "bear_researcher": "看跌研究員",
        "research_manager": "研究經理",

        # 交易團隊
        "trader": "交易員",

        # 風險管理團隊
        "risky_analyst": "激進分析師",
        "safe_analyst": "保守分析師",
        "neutral_analyst": "中立分析師",

        # 投資組合管理
        "portfolio_manager": "投資組合經理",

        # 團隊標題
        "analyst_team": "分析師團隊",
        "research_team": "研究團隊",
        "trading_team": "交易團隊",
        "risk_management": "風險管理",
        "portfolio_management": "投資組合管理",

        # 狀態
        "pending": "等待中",
        "in_progress": "進行中",
        "completed": "已完成",
        "error": "錯誤",

        # 報告標題
        "market_analysis": "市場分析",
        "social_sentiment": "社交情緒",
        "news_analysis": "新聞分析",
        "fundamentals_analysis": "基本面分析",
        "research_team_decision": "研究團隊決策",
        "trading_team_plan": "交易團隊計畫",
        "portfolio_management_decision": "投資組合管理決策",
        "bull_researcher_analysis": "看漲研究員分析",
        "bear_researcher_analysis": "看跌研究員分析",
        "research_manager_decision": "研究經理決策",
        "risky_analyst_analysis": "激進分析師分析",
        "safe_analyst_analysis": "保守分析師分析",
        "neutral_analyst_analysis": "中立分析師分析",

        # 完整報告標題
        "analyst_team_reports": "I. 分析師團隊報告",
        "research_team_reports": "II. 研究團隊決策",
        "trading_team_reports": "III. 交易團隊計畫",
        "risk_management_reports": "IV. 風險管理團隊決策",
        "portfolio_manager_reports": "V. 投資組合經理決策",

        # UI 元素
        "progress": "進度",
        "messages_tools": "訊息與工具",
        "current_report": "當前報告",
        "waiting_for_report": "等待分析報告...",
        "complete_analysis_report": "完整分析報告",

        # 統計
        "tool_calls": "工具調用",
        "llm_calls": "LLM 調用",
        "generated_reports": "已生成報告",

        # 訊息
        "selected_ticker": "已選擇股票代碼",
        "analysis_date": "分析日期",
        "selected_analysts": "已選擇分析師",
        "analyzing": "正在分析",
        "completed_analysis": "已完成分析",

        # 研究深度選項
        "shallow_research": "淺層 - 快速研究，少量辯論和策略討論回合",
        "medium_research": "中等 - 適中的辯論回合和策略討論",
        "deep_research": "深入 - 全面研究，深入的辯論和策略討論",

        # LLM 選擇
        "select_analysts_team": "選擇您的【分析師團隊】：",
        "select_research_depth": "選擇您的【研究深度】：",
        "select_quick_thinking_llm": "選擇您的【快速思考 LLM 引擎】：",
        "select_deep_thinking_llm": "選擇您的【深度思考 LLM 引擎】：",
        "select_llm_provider": "選擇您的 LLM 提供商：",

        # 指引訊息
        "space_to_select": "- 按空白鍵選擇/取消選擇分析師",
        "a_to_select_all": "- 按 'a' 鍵全選/取消全選",
        "enter_when_done": "- 按 Enter 鍵完成",
        "use_arrow_keys": "- 使用方向鍵導航",
        "press_enter_to_select": "- 按 Enter 鍵選擇",

        # 錯誤訊息
        "no_ticker_provided": "未提供股票代碼。退出中...",
        "no_date_provided": "未提供日期。退出中...",
        "no_analysts_selected": "未選擇分析師。退出中...",
        "no_research_depth_selected": "未選擇研究深度。退出中...",
        "no_shallow_thinking_selected": "未選擇快速思考 LLM 引擎。退出中...",
        "no_deep_thinking_selected": "未選擇深度思考 LLM 引擎。退出中...",
        "no_backend_selected": "未選擇 OpenAI 後端。退出中...",
        "invalid_ticker": "請輸入有效的股票代碼。",
        "invalid_date_format": "請輸入有效的日期格式 YYYY-MM-DD。",
        "must_select_one_analyst": "您必須至少選擇一位分析師。",
        "date_cannot_be_future": "錯誤：分析日期不能是未來日期",
        "invalid_date": "錯誤：無效的日期格式。請使用 YYYY-MM-DD",

        # 其他
        "default": "預設",
        "you_selected": "您選擇了",
        "url": "URL",
        "showing_last_messages": "顯示最後",
        "of": "條，共",
        "messages": "條訊息",
    },

    "zh_CN": {
        # 欢迎消息
        "welcome_title": "欢迎使用 TradingAgents",
        "welcome_subtitle": "多智能体 LLM 金融交易框架",
        "welcome_header": "TradingAgents：多智能体 LLM 金融交易框架 - CLI",
        "welcome_workflow": "工作流程步骤：",
        "welcome_workflow_steps": "I. 分析师团队 → II. 研究团队 → III. 交易员 → IV. 风险管理 → V. 投资组合管理",
        "built_by": "由 Tauric Research 构建",

        # 步骤标题
        "step_1_title": "步骤 1：股票代码",
        "step_1_prompt": "输入要分析的股票代码",
        "step_2_title": "步骤 2：分析日期",
        "step_2_prompt": "输入分析日期 (YYYY-MM-DD)",
        "step_3_title": "步骤 3：分析师团队",
        "step_3_prompt": "选择您的 LLM 分析师智能体进行分析",
        "step_4_title": "步骤 4：研究深度",
        "step_4_prompt": "选择您的研究深度层级",
        "step_5_title": "步骤 5：OpenAI 后端",
        "step_5_prompt": "选择要使用的服务",
        "step_6_title": "步骤 6：思考智能体",
        "step_6_prompt": "选择您的思考智能体进行分析",

        # 分析师类型
        "market_analyst": "市场分析师",
        "social_analyst": "社交媒体分析师",
        "news_analyst": "新闻分析师",
        "fundamentals_analyst": "基本面分析师",

        # 研究团队
        "bull_researcher": "看涨研究员",
        "bear_researcher": "看跌研究员",
        "research_manager": "研究经理",

        # 交易团队
        "trader": "交易员",

        # 风险管理团队
        "risky_analyst": "激进分析师",
        "safe_analyst": "保守分析师",
        "neutral_analyst": "中立分析师",

        # 投资组合管理
        "portfolio_manager": "投资组合经理",

        # 团队标题
        "analyst_team": "分析师团队",
        "research_team": "研究团队",
        "trading_team": "交易团队",
        "risk_management": "风险管理",
        "portfolio_management": "投资组合管理",

        # 状态
        "pending": "等待中",
        "in_progress": "进行中",
        "completed": "已完成",
        "error": "错误",

        # 报告标题
        "market_analysis": "市场分析",
        "social_sentiment": "社交情绪",
        "news_analysis": "新闻分析",
        "fundamentals_analysis": "基本面分析",
        "research_team_decision": "研究团队决策",
        "trading_team_plan": "交易团队计划",
        "portfolio_management_decision": "投资组合管理决策",
        "bull_researcher_analysis": "看涨研究员分析",
        "bear_researcher_analysis": "看跌研究员分析",
        "research_manager_decision": "研究经理决策",
        "risky_analyst_analysis": "激进分析师分析",
        "safe_analyst_analysis": "保守分析师分析",
        "neutral_analyst_analysis": "中立分析师分析",

        # 完整报告标题
        "analyst_team_reports": "I. 分析师团队报告",
        "research_team_reports": "II. 研究团队决策",
        "trading_team_reports": "III. 交易团队计划",
        "risk_management_reports": "IV. 风险管理团队决策",
        "portfolio_manager_reports": "V. 投资组合经理决策",

        # UI 元素
        "progress": "进度",
        "messages_tools": "消息与工具",
        "current_report": "当前报告",
        "waiting_for_report": "等待分析报告...",
        "complete_analysis_report": "完整分析报告",

        # 统计
        "tool_calls": "工具调用",
        "llm_calls": "LLM 调用",
        "generated_reports": "已生成报告",

        # 消息
        "selected_ticker": "已选择股票代码",
        "analysis_date": "分析日期",
        "selected_analysts": "已选择分析师",
        "analyzing": "正在分析",
        "completed_analysis": "已完成分析",

        # 研究深度选项
        "shallow_research": "浅层 - 快速研究，少量辩论和策略讨论回合",
        "medium_research": "中等 - 适中的辩论回合和策略讨论",
        "deep_research": "深入 - 全面研究，深入的辩论和策略讨论",

        # LLM 选择
        "select_analysts_team": "选择您的【分析师团队】：",
        "select_research_depth": "选择您的【研究深度】：",
        "select_quick_thinking_llm": "选择您的【快速思考 LLM 引擎】：",
        "select_deep_thinking_llm": "选择您的【深度思考 LLM 引擎】：",
        "select_llm_provider": "选择您的 LLM 提供商：",

        # 指引消息
        "space_to_select": "- 按空格键选择/取消选择分析师",
        "a_to_select_all": "- 按 'a' 键全选/取消全选",
        "enter_when_done": "- 按 Enter 键完成",
        "use_arrow_keys": "- 使用方向键导航",
        "press_enter_to_select": "- 按 Enter 键选择",

        # 错误消息
        "no_ticker_provided": "未提供股票代码。退出中...",
        "no_date_provided": "未提供日期。退出中...",
        "no_analysts_selected": "未选择分析师。退出中...",
        "no_research_depth_selected": "未选择研究深度。退出中...",
        "no_shallow_thinking_selected": "未选择快速思考 LLM 引擎。退出中...",
        "no_deep_thinking_selected": "未选择深度思考 LLM 引擎。退出中...",
        "no_backend_selected": "未选择 OpenAI 后端。退出中...",
        "invalid_ticker": "请输入有效的股票代码。",
        "invalid_date_format": "请输入有效的日期格式 YYYY-MM-DD。",
        "must_select_one_analyst": "您必须至少选择一位分析师。",
        "date_cannot_be_future": "错误：分析日期不能是未来日期",
        "invalid_date": "错误：无效的日期格式。请使用 YYYY-MM-DD",

        # 其他
        "default": "默认",
        "you_selected": "您选择了",
        "url": "URL",
        "showing_last_messages": "显示最后",
        "of": "条，共",
        "messages": "条消息",
    },

    "en_US": {
        # Welcome messages
        "welcome_title": "Welcome to TradingAgents",
        "welcome_subtitle": "Multi-Agents LLM Financial Trading Framework",
        "welcome_header": "TradingAgents: Multi-Agents LLM Financial Trading Framework - CLI",
        "welcome_workflow": "Workflow Steps:",
        "welcome_workflow_steps": "I. Analyst Team → II. Research Team → III. Trader → IV. Risk Management → V. Portfolio Management",
        "built_by": "Built by Tauric Research",

        # Step titles
        "step_1_title": "Step 1: Ticker Symbol",
        "step_1_prompt": "Enter the ticker symbol to analyze",
        "step_2_title": "Step 2: Analysis Date",
        "step_2_prompt": "Enter the analysis date (YYYY-MM-DD)",
        "step_3_title": "Step 3: Analysts Team",
        "step_3_prompt": "Select your LLM analyst agents for the analysis",
        "step_4_title": "Step 4: Research Depth",
        "step_4_prompt": "Select your research depth level",
        "step_5_title": "Step 5: OpenAI backend",
        "step_5_prompt": "Select which service to talk to",
        "step_6_title": "Step 6: Thinking Agents",
        "step_6_prompt": "Select your thinking agents for analysis",

        # Analyst types
        "market_analyst": "Market Analyst",
        "social_analyst": "Social Analyst",
        "news_analyst": "News Analyst",
        "fundamentals_analyst": "Fundamentals Analyst",

        # Research team
        "bull_researcher": "Bull Researcher",
        "bear_researcher": "Bear Researcher",
        "research_manager": "Research Manager",

        # Trading team
        "trader": "Trader",

        # Risk management team
        "risky_analyst": "Risky Analyst",
        "safe_analyst": "Safe Analyst",
        "neutral_analyst": "Neutral Analyst",

        # Portfolio management
        "portfolio_manager": "Portfolio Manager",

        # Team titles
        "analyst_team": "Analyst Team",
        "research_team": "Research Team",
        "trading_team": "Trading Team",
        "risk_management": "Risk Management",
        "portfolio_management": "Portfolio Management",

        # Status
        "pending": "pending",
        "in_progress": "in_progress",
        "completed": "completed",
        "error": "error",

        # Report titles
        "market_analysis": "Market Analysis",
        "social_sentiment": "Social Sentiment",
        "news_analysis": "News Analysis",
        "fundamentals_analysis": "Fundamentals Analysis",
        "research_team_decision": "Research Team Decision",
        "trading_team_plan": "Trading Team Plan",
        "portfolio_management_decision": "Portfolio Management Decision",
        "bull_researcher_analysis": "Bull Researcher Analysis",
        "bear_researcher_analysis": "Bear Researcher Analysis",
        "research_manager_decision": "Research Manager Decision",
        "risky_analyst_analysis": "Risky Analyst Analysis",
        "safe_analyst_analysis": "Safe Analyst Analysis",
        "neutral_analyst_analysis": "Neutral Analyst Analysis",

        # Complete report titles
        "analyst_team_reports": "I. Analyst Team Reports",
        "research_team_reports": "II. Research Team Decision",
        "trading_team_reports": "III. Trading Team Plan",
        "risk_management_reports": "IV. Risk Management Team Decision",
        "portfolio_manager_reports": "V. Portfolio Manager Decision",

        # UI elements
        "progress": "Progress",
        "messages_tools": "Messages & Tools",
        "current_report": "Current Report",
        "waiting_for_report": "Waiting for analysis report...",
        "complete_analysis_report": "Complete Analysis Report",

        # Statistics
        "tool_calls": "Tool Calls",
        "llm_calls": "LLM Calls",
        "generated_reports": "Generated Reports",

        # Messages
        "selected_ticker": "Selected ticker",
        "analysis_date": "Analysis date",
        "selected_analysts": "Selected analysts",
        "analyzing": "Analyzing",
        "completed_analysis": "Completed analysis for",

        # Research depth options
        "shallow_research": "Shallow - Quick research, few debate and strategy discussion rounds",
        "medium_research": "Medium - Middle ground, moderate debate rounds and strategy discussion",
        "deep_research": "Deep - Comprehensive research, in depth debate and strategy discussion",

        # LLM selection
        "select_analysts_team": "Select Your [Analysts Team]:",
        "select_research_depth": "Select Your [Research Depth]:",
        "select_quick_thinking_llm": "Select Your [Quick-Thinking LLM Engine]:",
        "select_deep_thinking_llm": "Select Your [Deep-Thinking LLM Engine]:",
        "select_llm_provider": "Select your LLM Provider:",

        # Instruction messages
        "space_to_select": "- Press Space to select/unselect analysts",
        "a_to_select_all": "- Press 'a' to select/unselect all",
        "enter_when_done": "- Press Enter when done",
        "use_arrow_keys": "- Use arrow keys to navigate",
        "press_enter_to_select": "- Press Enter to select",

        # Error messages
        "no_ticker_provided": "No ticker symbol provided. Exiting...",
        "no_date_provided": "No date provided. Exiting...",
        "no_analysts_selected": "No analysts selected. Exiting...",
        "no_research_depth_selected": "No research depth selected. Exiting...",
        "no_shallow_thinking_selected": "No shallow thinking llm engine selected. Exiting...",
        "no_deep_thinking_selected": "No deep thinking llm engine selected. Exiting...",
        "no_backend_selected": "no OpenAI backend selected. Exiting...",
        "invalid_ticker": "Please enter a valid ticker symbol.",
        "invalid_date_format": "Please enter a valid date in YYYY-MM-DD format.",
        "must_select_one_analyst": "You must select at least one analyst.",
        "date_cannot_be_future": "Error: Analysis date cannot be in the future",
        "invalid_date": "Error: Invalid date format. Please use YYYY-MM-DD",

        # Other
        "default": "Default",
        "you_selected": "You selected",
        "url": "URL",
        "showing_last_messages": "Showing last",
        "of": "of",
        "messages": "messages",
    }
}


class I18n:
    """國際化管理器"""

    def __init__(self, language: str = None):
        """
        初始化 I18n 管理器

        Args:
            language: 語言代碼 (zh_TW, zh_CN, en_US)
                     如果未指定，會從環境變數 TRADINGAGENTS_LANG 讀取
                     預設為繁體中文 (zh_TW)
        """
        if language is None:
            language = os.environ.get("TRADINGAGENTS_LANG", "zh_TW")

        self.language = language
        self.translations = TRANSLATIONS.get(language, TRANSLATIONS["zh_TW"])

    def t(self, key: str, default: str = None) -> str:
        """
        取得翻譯文字

        Args:
            key: 翻譯鍵
            default: 如果找不到翻譯時的預設值

        Returns:
            翻譯後的文字，如果找不到則返回 default 或 key
        """
        return self.translations.get(key, default or key)

    def __call__(self, key: str, default: str = None) -> str:
        """簡寫方式呼叫翻譯"""
        return self.t(key, default)


# 全域 i18n 實例
# 可以透過環境變數 TRADINGAGENTS_LANG 設定語言
# 例如：export TRADINGAGENTS_LANG=zh_TW  # 繁體中文
#      export TRADINGAGENTS_LANG=zh_CN  # 簡體中文
#      export TRADINGAGENTS_LANG=en_US  # 英文
i18n = I18n()
