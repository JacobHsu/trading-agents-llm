#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自動化分析腳本 - 用於 GitHub Actions
無需用戶交互，直接生成分析報告
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加項目路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from cli.html_report_generator import HTMLReportGenerator


def main():
    parser = argparse.ArgumentParser(description='自動化股票分析')
    parser.add_argument('--ticker', default='SPY', help='股票代碼 (默認: SPY)')
    parser.add_argument('--date', default=None, help='分析日期 YYYY-MM-DD (默認: 今天)')
    parser.add_argument('--output', default='index.html', help='輸出文件路徑 (默認: index.html)')
    parser.add_argument('--analysts', default='market,news,fundamentals',
                       help='分析師類型，逗號分隔 (默認: market,news,fundamentals)')

    args = parser.parse_args()

    # 獲取分析日期
    analysis_date = args.date or datetime.now().strftime("%Y-%m-%d")

    # 解析分析師類型
    analysts = [a.strip() for a in args.analysts.split(',')]

    print(f"="*60)
    print(f"自動化分析啟動")
    print(f"="*60)
    print(f"股票代碼: {args.ticker}")
    print(f"分析日期: {analysis_date}")
    print(f"分析師: {', '.join(analysts)}")
    print(f"輸出文件: {args.output}")
    print(f"="*60)

    # 創建配置
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1

    # 初始化圖
    print("\n初始化分析系統...")
    graph = TradingAgentsGraph(analysts, config=config, debug=False)

    # 創建初始狀態
    print(f"\n開始分析 {args.ticker}...")
    init_state = graph.propagator.create_initial_state(args.ticker, analysis_date)
    graph_args = graph.propagator.get_graph_args()

    # 運行分析
    trace = []
    try:
        for i, chunk in enumerate(graph.graph.stream(init_state, **graph_args), 1):
            trace.append(chunk)
            if i % 5 == 0:
                print(f"  處理步驟 {i}...")
    except Exception as e:
        print(f"\n✗ 分析過程出錯: {e}")
        raise

    print(f"\n分析完成，共 {len(trace)} 個步驟")

    if not trace:
        raise RuntimeError("分析未產生任何結果")

    # 獲取最終狀態
    final_state = trace[-1]
    print(f"最終狀態類型: {type(final_state)}")

    # 從最終狀態中提取實際的狀態字典
    # LangGraph 返回的是 {node_name: state_dict} 的格式
    if isinstance(final_state, dict):
        # 獲取最後一個節點的狀態
        state_values = list(final_state.values())
        if state_values:
            actual_state = state_values[0]
        else:
            actual_state = final_state
    else:
        actual_state = final_state

    print(f"實際狀態鍵值: {list(actual_state.keys()) if isinstance(actual_state, dict) else 'N/A'}")

    # 收集報告內容
    reports = {
        "market_report": actual_state.get("market_report", ""),
        "sentiment_report": actual_state.get("sentiment_report", ""),
        "news_report": actual_state.get("news_report", ""),
        "fundamentals_report": actual_state.get("fundamentals_report", ""),
        "investment_plan": actual_state.get("investment_plan", ""),
        "trader_investment_plan": actual_state.get("trader_investment_plan", ""),
        "final_trade_decision": actual_state.get("final_trade_decision", ""),
    }

    # 檢查是否有任何報告內容
    has_content = any(reports.values())
    print(f"報告內容檢查: {'有內容' if has_content else '無內容'}")

    # 生成 HTML 報告
    print(f"\n生成 HTML 報告...")
    try:
        html_generator = HTMLReportGenerator(llm=graph.quick_thinking_llm)

        output_path = html_generator.generate_html(
            ticker=args.ticker,
            analysis_date=analysis_date,
            reports=reports,
            output_path=args.output
        )

        print(f"\n✓ 報告已生成: {output_path}")

        # 驗證文件是否存在
        from pathlib import Path
        if not Path(output_path).exists():
            raise RuntimeError(f"報告文件未成功創建: {output_path}")

        file_size = Path(output_path).stat().st_size
        print(f"文件大小: {file_size:,} bytes")

    except Exception as e:
        print(f"\n✗ 生成 HTML 報告時出錯: {e}")
        raise

    print(f"="*60)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n✗ 錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
