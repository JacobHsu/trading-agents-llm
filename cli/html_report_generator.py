"""
HTML 報告生成器
將英文分析報告翻譯成中文並生成 HTML 文件
"""

import os
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path


class HTMLReportGenerator:
    """
    生成中文 HTML 分析報告
    """

    def __init__(self, llm=None):
        """
        初始化報告生成器

        Args:
            llm: LangChain LLM 實例，用於翻譯
        """
        self.llm = llm
        self.lang = os.environ.get("TRADINGAGENTS_LANG", "zh_TW")
        self.target_lang = "繁體中文" if self.lang == "zh_TW" else "簡體中文" if self.lang == "zh_CN" else "English"

    def translate_text(self, text: str) -> str:
        """
        翻譯文本

        Args:
            text: 英文文本

        Returns:
            翻譯後的文本
        """
        # 如果是英文模式或沒有 LLM，直接返回原文
        if self.lang == "en_US" or not self.llm or not text:
            return text

        # 如果文本太短，不翻譯
        if len(text.strip()) < 10:
            return text

        # 構建翻譯 prompt
        translation_prompt = f"""請將以下英文金融分析報告翻譯成{self.target_lang}。

要求：
1. 保持專業術語的準確性
2. 保持原文的段落和格式結構
3. 保持數字、百分比、日期、股票代碼不變
4. 保持專業性和可讀性
5. 只輸出翻譯結果，不要添加任何說明或前綴

原文：
{text}

翻譯："""

        try:
            # 調用 LLM 進行翻譯
            response = self.llm.invoke(translation_prompt)

            # 提取翻譯結果
            if hasattr(response, 'content'):
                translated = response.content.strip()
            else:
                translated = str(response).strip()

            return translated

        except Exception as e:
            # 翻譯失敗，返回原文
            print(f"翻譯失敗: {e}")
            return text

    def generate_html(
        self,
        ticker: str,
        analysis_date: str,
        reports: Dict[str, str],
        output_path: str = "analysis_report.html"
    ) -> str:
        """
        生成 HTML 報告

        Args:
            ticker: 股票代碼
            analysis_date: 分析日期
            reports: 報告內容字典
            output_path: 輸出文件路徑

        Returns:
            生成的 HTML 文件路徑
        """
        # 翻譯所有報告內容
        print(f"\n正在翻譯報告內容為{self.target_lang}...")
        translated_reports = {}

        section_names = {
            "market_report": "市場分析報告" if self.lang != "en_US" else "Market Analysis Report",
            "sentiment_report": "社交媒體情緒分析" if self.lang != "en_US" else "Social Media Sentiment Analysis",
            "news_report": "新聞分析報告" if self.lang != "en_US" else "News Analysis Report",
            "fundamentals_report": "基本面分析報告" if self.lang != "en_US" else "Fundamentals Analysis Report",
            "investment_plan": "研究團隊投資計劃" if self.lang != "en_US" else "Research Team Investment Plan",
            "trader_investment_plan": "交易團隊計劃" if self.lang != "en_US" else "Trading Team Plan",
            "final_trade_decision": "投資組合管理決策" if self.lang != "en_US" else "Portfolio Management Decision",
        }

        for section_key, content in reports.items():
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            if content:
                print(f"  翻譯 {section_names.get(section_key, section_key)}...")
                translated_reports[section_key] = self.translate_text(content)
            else:
                translated_reports[section_key] = content

        # 生成 HTML
        html_content = self._generate_html_template(
            ticker, analysis_date, translated_reports, section_names
        )

        # 寫入文件
        output_file = Path(output_path)
        output_file.write_text(html_content, encoding='utf-8')

        print(f"\nHTML 報告已生成: {output_file.absolute()}")
        return str(output_file.absolute())

    def _generate_html_template(
        self,
        ticker: str,
        analysis_date: str,
        reports: Dict[str, str],
        section_names: Dict[str, str]
    ) -> str:
        """
        生成 HTML 模板

        Args:
            ticker: 股票代碼
            analysis_date: 分析日期
            reports: 翻譯後的報告內容
            section_names: 章節名稱

        Returns:
            HTML 內容
        """
        title = f"{ticker} 投資分析報告" if self.lang != "en_US" else f"{ticker} Investment Analysis Report"
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 構建報告內容
        report_sections_html = ""

        # I. 分析師團隊報告
        analyst_title = "I. 分析師團隊報告" if self.lang != "en_US" else "I. Analyst Team Reports"
        report_sections_html += f'<h2 class="team-title">{analyst_title}</h2>\n'

        for key in ["market_report", "sentiment_report", "news_report", "fundamentals_report"]:
            if key in reports and reports[key]:
                report_sections_html += f'''
        <div class="report-section">
            <h3>{section_names[key]}</h3>
            <div class="report-content">{self._format_content(reports[key])}</div>
        </div>
        '''

        # II. 研究團隊報告
        if "investment_plan" in reports and reports["investment_plan"]:
            research_title = "II. 研究團隊報告" if self.lang != "en_US" else "II. Research Team Reports"
            report_sections_html += f'<h2 class="team-title">{research_title}</h2>\n'
            report_sections_html += f'''
        <div class="report-section">
            <h3>{section_names["investment_plan"]}</h3>
            <div class="report-content">{self._format_content(reports["investment_plan"])}</div>
        </div>
        '''

        # III. 交易團隊報告
        if "trader_investment_plan" in reports and reports["trader_investment_plan"]:
            trading_title = "III. 交易團隊報告" if self.lang != "en_US" else "III. Trading Team Reports"
            report_sections_html += f'<h2 class="team-title">{trading_title}</h2>\n'
            report_sections_html += f'''
        <div class="report-section">
            <h3>{section_names["trader_investment_plan"]}</h3>
            <div class="report-content">{self._format_content(reports["trader_investment_plan"])}</div>
        </div>
        '''

        # IV. 投資組合管理報告
        if "final_trade_decision" in reports and reports["final_trade_decision"]:
            portfolio_title = "IV. 投資組合管理報告" if self.lang != "en_US" else "IV. Portfolio Management Reports"
            report_sections_html += f'<h2 class="team-title">{portfolio_title}</h2>\n'
            report_sections_html += f'''
        <div class="report-section highlight">
            <h3>{section_names["final_trade_decision"]}</h3>
            <div class="report-content">{self._format_content(reports["final_trade_decision"])}</div>
        </div>
        '''

        # 完整的 HTML
        html = f'''<!DOCTYPE html>
<html lang="{self.lang[:2]}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {analysis_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "微軟正黑體", sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .team-title {{
            font-size: 1.8em;
            color: #667eea;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .report-section {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 25px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .report-section.highlight {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            border-left: 4px solid #d63031;
        }}

        .report-section h3 {{
            font-size: 1.4em;
            color: #2d3436;
            margin-bottom: 15px;
            font-weight: 600;
        }}

        .report-content {{
            font-size: 1.05em;
            line-height: 1.8;
            color: #2d3436;
        }}

        .report-content strong {{
            color: #667eea;
            font-weight: 700;
        }}

        .report-content em {{
            font-style: italic;
            color: #636e72;
        }}

        .report-content h1, .report-content h2, .report-content h3, .report-content h4 {{
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        .report-content ul, .report-content ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}

        .report-content li {{
            margin: 5px 0;
        }}

        .report-content p {{
            margin: 10px 0;
            line-height: 1.8;
        }}

        .decision-buy {{
            display: inline-block;
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1.1em;
            box-shadow: 0 4px 15px rgba(0, 184, 148, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .decision-sell {{
            display: inline-block;
            background: linear-gradient(135deg, #d63031 0%, #ff7675 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1.1em;
            box-shadow: 0 4px 15px rgba(214, 48, 49, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .decision-hold {{
            display: inline-block;
            background: linear-gradient(135deg, #fdcb6e 0%, #ffeaa7 100%);
            color: #2d3436;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 1.1em;
            box-shadow: 0 4px 15px rgba(253, 203, 110, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        footer {{
            background: #2d3436;
            color: #b2bec3;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}

            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 {title}</h1>
            <div class="meta">
                <p>股票代碼: <strong>{ticker}</strong> | 分析日期: <strong>{analysis_date}</strong></p>
                <p>報告生成時間: {generated_time}</p>
            </div>
        </header>

        <div class="content">
            {report_sections_html}
        </div>

        <footer>
            <p>© {datetime.now().year} TradingAgents - 由 AI 多代理系統生成</p>
            <p>本報告僅供參考，不構成投資建議</p>
        </footer>
    </div>
</body>
</html>'''

        return html

    def _format_content(self, content: str) -> str:
        """
        格式化內容為 HTML - 將 Markdown 轉換為 HTML

        Args:
            content: Markdown 文本內容

        Returns:
            HTML 格式的內容
        """
        import re

        # 先轉義 HTML 特殊字符
        content = content.replace('&', '&amp;')
        content = content.replace('<', '&lt;')
        content = content.replace('>', '&gt;')

        # 處理 Markdown 表格（在處理標題之前）
        content = self._convert_markdown_table(content)

        # 處理標題
        content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'<h3 style="color: #667eea; margin-top: 20px; margin-bottom: 10px;">\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2 style="color: #667eea; margin-top: 25px; margin-bottom: 12px;">\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^# (.+)$', r'<h1 style="color: #667eea; margin-top: 30px; margin-bottom: 15px;">\1</h1>', content, flags=re.MULTILINE)

        # 高亮 BUY/SELL/HOLD（在處理粗體之前）
        content = content.replace('**BUY**', '<span class="decision-buy">買入(BUY)</span>')
        content = content.replace('**SELL**', '<span class="decision-sell">賣出(SELL)</span>')
        content = content.replace('**HOLD**', '<span class="decision-hold">持有(HOLD)</span>')

        # 處理粗體 **text**
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)

        # 處理斜體 *text*
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)

        # 處理無序列表
        lines = content.split('\n')
        in_ul = False
        result_lines = []

        for line in lines:
            # 檢查是否是列表項
            if re.match(r'^\s*[-*]\s+', line):
                list_content = re.sub(r'^\s*[-*]\s+', '', line)
                if not in_ul:
                    result_lines.append('<ul style="margin: 10px 0; padding-left: 30px;">')
                    in_ul = True
                result_lines.append(f'<li style="margin: 5px 0;">{list_content}</li>')
            else:
                if in_ul:
                    result_lines.append('</ul>')
                    in_ul = False
                result_lines.append(line)

        if in_ul:
            result_lines.append('</ul>')

        content = '\n'.join(result_lines)

        # 處理有序列表
        lines = content.split('\n')
        in_ol = False
        result_lines = []

        for line in lines:
            # 檢查是否是有序列表項
            if re.match(r'^\s*\d+\.\s+', line):
                list_content = re.sub(r'^\s*\d+\.\s+', '', line)
                if not in_ol:
                    result_lines.append('<ol style="margin: 10px 0; padding-left: 30px;">')
                    in_ol = True
                result_lines.append(f'<li style="margin: 5px 0;">{list_content}</li>')
            else:
                if in_ol:
                    result_lines.append('</ol>')
                    in_ol = False
                result_lines.append(line)

        if in_ol:
            result_lines.append('</ol>')

        content = '\n'.join(result_lines)

        # 處理段落（連續的非空行作為段落）
        lines = content.split('\n')
        result_lines = []
        paragraph = []

        for line in lines:
            stripped = line.strip()
            # 如果是 HTML 標籤開頭，不作為段落處理
            if stripped.startswith('<'):
                if paragraph:
                    result_lines.append(f'<p style="margin: 10px 0; line-height: 1.8;">{" ".join(paragraph)}</p>')
                    paragraph = []
                result_lines.append(line)
            elif stripped == '':
                if paragraph:
                    result_lines.append(f'<p style="margin: 10px 0; line-height: 1.8;">{" ".join(paragraph)}</p>')
                    paragraph = []
                result_lines.append(line)
            else:
                paragraph.append(line)

        if paragraph:
            result_lines.append(f'<p style="margin: 10px 0; line-height: 1.8;">{" ".join(paragraph)}</p>')

        content = '\n'.join(result_lines)

        return content

    def _convert_markdown_table(self, content: str) -> str:
        """
        將 Markdown 表格轉換為 HTML 表格

        Args:
            content: 包含 Markdown 表格的文本

        Returns:
            轉換後的 HTML 內容
        """
        import re

        lines = content.split('\n')
        result_lines = []
        in_table = False
        table_rows = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # 檢查是否是表格行（包含 | 符號）
            if '|' in line and line.count('|') >= 2:
                # 檢查下一行是否是分隔符行（例如 | :--- | :---: | ---: |）
                is_table_start = False
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    # 分隔符行包含 - 和可選的 :
                    if re.match(r'^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$', next_line):
                        is_table_start = True
                        in_table = True
                        table_rows = []

                        # 添加表頭
                        header_cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                        table_rows.append(('header', header_cells))

                        # 跳過分隔符行
                        i += 2
                        continue

                # 如果在表格中，添加數據行
                if in_table:
                    data_cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                    if data_cells:
                        table_rows.append(('data', data_cells))
                    else:
                        # 空行，表格結束
                        in_table = False
                        result_lines.append(self._build_html_table(table_rows))
                        table_rows = []
                else:
                    result_lines.append(lines[i])
            else:
                # 非表格行
                if in_table and table_rows:
                    # 結束當前表格
                    in_table = False
                    result_lines.append(self._build_html_table(table_rows))
                    table_rows = []
                result_lines.append(lines[i])

            i += 1

        # 處理最後一個表格
        if in_table and table_rows:
            result_lines.append(self._build_html_table(table_rows))

        return '\n'.join(result_lines)

    def _build_html_table(self, table_rows) -> str:
        """
        構建 HTML 表格

        Args:
            table_rows: 表格行列表，每個元素是 (row_type, cells) 元組

        Returns:
            HTML 表格字符串
        """
        if not table_rows:
            return ''

        html = '<table style="width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">\n'

        # 處理表頭
        has_header = False
        for row_type, cells in table_rows:
            if row_type == 'header':
                html += '  <thead>\n    <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">\n'
                for cell in cells:
                    html += f'      <th style="padding: 12px 15px; text-align: left; font-weight: 600; border: 1px solid #ddd;">{cell}</th>\n'
                html += '    </tr>\n  </thead>\n'
                has_header = True
                break

        # 處理數據行
        html += '  <tbody>\n'
        for row_type, cells in table_rows:
            if row_type == 'data':
                html += '    <tr style="background-color: #f8f9fa;">\n'
                for cell in cells:
                    html += f'      <td style="padding: 12px 15px; border: 1px solid #ddd; color: #2d3436;">{cell}</td>\n'
                html += '    </tr>\n'
        html += '  </tbody>\n'

        html += '</table>\n'
        return html
