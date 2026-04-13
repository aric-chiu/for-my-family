# -*- coding: utf-8 -*-
"""
掃描 gh-pages/ 下所有 {code}_analysis_{YYYYMMDD}.html，
自動產出按日期分組的首頁索引 index.html。
新報告由分析流程直接產出帶日期的 HTML，本腳本只負責重建索引。
"""
import sys, io, os, re, glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPORTS_DIR = os.path.dirname(os.path.abspath(__file__))

# 股票名稱對照（新股票分析時會自動加入）
STOCK_NAMES = {
    "2367": "燿華電子",
    "6405": "悅城科技",
    "6509": "聚和國際",
    "6547": "高端疫苗",
    "7709": "榮田精機",
    "MU": "美光科技",
    "NVDA": "輝達",
    "NET": "Cloudflare",
}

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>股票分析報告</title>
<style>
  body {{
    font-family: -apple-system, "Microsoft JhengHei", "Segoe UI", sans-serif;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background: #f8f9fa;
    color: #333;
    line-height: 1.6;
  }}
  h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 8px; }}
  h2 {{ color: #444; margin-top: 32px; border-left: 4px solid #1a73e8; padding-left: 12px; }}
  .card {{
    background: white;
    border-radius: 8px;
    padding: 12px 20px;
    margin: 8px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .card a {{
    color: #1a73e8;
    text-decoration: none;
    font-size: 16px;
    font-weight: bold;
  }}
  .card a:hover {{ text-decoration: underline; }}
  .card .code {{ color: #888; font-size: 13px; }}
  .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #ddd; color: #888; font-size: 12px; }}
</style>
</head>
<body>
<h1>📊 股票分析報告</h1>
<p>箱波均控盤戰法 · 分析報告索引</p>
{sections}
<div class="footer">箱波均控盤戰法分析報告 · 由 Claude Code 自動產出</div>
</body>
</html>"""

# 掃描所有帶日期的報告 HTML
pattern = re.compile(r'^([A-Za-z0-9]+)_analysis_(\d{8})\.html$')
by_date = defaultdict(list)

for fname in os.listdir(REPORTS_DIR):
    m = pattern.match(fname)
    if m:
        code, date_str = m.group(1), m.group(2)
        display_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        name = STOCK_NAMES.get(code, code)
        by_date[display_date].append((code, name, fname))

# 按日期降序排列（最新在上）
sections_html = ""
for date in sorted(by_date.keys(), reverse=True):
    entries = sorted(by_date[date], key=lambda x: x[0])
    sections_html += f"\n<h2>{date}</h2>\n"
    for code, name, fname in entries:
        sections_html += f"""<div class="card">
  <a href="{fname}">{code} {name}</a>
  <span class="code">{fname}</span>
</div>\n"""

with open(os.path.join(REPORTS_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(INDEX_TEMPLATE.format(sections=sections_html))

print(f"已掃描 {sum(len(v) for v in by_date.values())} 份報告，{len(by_date)} 個日期")
print("已產出: index.html")
