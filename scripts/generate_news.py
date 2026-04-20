import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import re

# ==============================================
# 1. 配置：抓取源（RSS + GitHub API）
# ==============================================
FEEDS = [
    # 框架/工具官方博客
    {"name": "Vue Blog", "url": "https://vuejs.org/feed.xml", "type": "framework"},
    {"name": "React Blog", "url": "https://react.dev/feed.xml", "type": "framework"},
    {"name": "Vite Blog", "url": "https://vitejs.dev/feed.xml", "type": "tool"},
    {"name": "MDN", "url": "https://developer.mozilla.org/en-US/blog/rss.xml", "type": "web"},
    # 前端资讯聚合
    {"name": "前端之巅", "url": "https://rsshub.app/frontend-trends", "type": "general"},
    {"name": "掘金前端", "url": "https://rsshub.app/juejin/frontend", "type": "general"},
    # GitHub Trending 前端
    {"name": "GitHub Trending", "url": "https://github.com/trending/frontend?since=daily", "type": "github"},
]

# 关键词过滤（只保留前端核心）
KEYWORDS = [
    "vue", "react", "angular", "svelte", "solid",
    "vite", "rspack", "turbopack", "webpack",
    "ai", "llm", "组件", "低代码",
    "css", "html", "web api", "浏览器",
    "uniapp", "taro", "flutter", "微前端",
    "字节", "阿里", "腾讯", "美团",
    "开源", "组件库", "可视化"
]

# ==============================================
# 2. 工具函数
# ==============================================
def is_recent(entry, days=1):
    """判断是否是前1天内的文章"""
    try:
        if hasattr(entry, 'published_parsed'):
            pub = datetime(*entry.published_parsed[:6])
            return datetime.now() - pub < timedelta(days=days)
    except:
        pass
    return False

def clean_text(s):
    """清理文本，精简到60字内"""
    s = re.sub(r'<.*?>', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:57] + '...' if len(s) > 60 else s

def get_keyword(title, summary):
    """提取2-4字关键词（按你Skill要求）"""
    text = (title + ' ' + summary).lower()
    for kw in ["Vue", "React", "Vite", "AI", "CSS", "Web", "跨端", "大厂", "开源"]:
        if kw.lower() in text:
            return kw
    return "前端动态"

# ==============================================
# 3. 抓取所有源
# ==============================================
items = []
for source in FEEDS:
    try:
        if source["type"] == "github":
            # 简易抓取 GitHub Trending
            res = requests.get(source["url"], timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            repos = soup.select("h2.h3 a")[:3]
            for r in repos:
                items.append({
                    "title": r.get_text(strip=True),
                    "link": "https://github.com" + r["href"],
                    "summary": "GitHub Trending 热门前端项目",
                    "source": source["name"],
                    "time": datetime.now()
                })
        else:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:10]:
                if not is_recent(entry):
                    continue
                title = entry.title
                summary = entry.get("summary", "")
                text = (title + " " + summary).lower()
                if not any(kw in text for kw in KEYWORDS):
                    continue
                items.append({
                    "title": title,
                    "link": entry.link,
                    "summary": summary,
                    "source": source["name"],
                    "time": datetime.now()
                })
    except Exception as e:
        print(f"抓取 {source['name']} 失败: {e}")

# 去重（按链接）
seen = set()
unique = []
for item in items:
    if item["link"] not in seen:
        seen.add(item["link"])
        unique.append(item)

# 取前8条（按你Skill）
final = unique[:8]

# ==============================================
# 4. 按你Skill格式生成MD
# ==============================================
today = datetime.now().strftime("%Y年%m月%d日")
md_lines = [f"【{today} 前端行业核心动态汇总】"]

for i, item in enumerate(final, 1):
    kw = get_keyword(item["title"], item["summary"])
    title = clean_text(item["title"])
    link = item["link"]
    source = item["source"]
    line = f"{i}. 「{kw}」：[{title}]({link})（{source}）"
    md_lines.append(line)

md_content = "\n".join(md_lines)

# ==============================================
# 5. 写入文件（按日期）
# ==============================================
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"daily/{date_str}-frontend.md"
os.makedirs("daily", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"✅ 生成完成：{filename}")
print(f"✅ 共 {len(final)} 条动态")
