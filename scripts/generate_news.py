import os
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# -------------------------- 配置信息 --------------------------
today = datetime.now()
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
week_num = f"{today.year}-{today.isocalendar()[1]-1}周"
week_str = f"{last_monday.strftime('%Y-%m-%d')} 至 {last_sunday.strftime('%Y-%m-%d')}"
md_file_name = f"{week_num}（{last_monday.strftime('%m%d')}-{last_sunday.strftime('%m%d')}）.md"

# 路径配置
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, "docs", str(today.year))
os.makedirs(docs_dir, exist_ok=True)
md_file_path = os.path.join(docs_dir, md_file_name)

# 资讯源配置（精选高价值、更新稳定的前端源）
NEWS_SOURCES = {
    "vue_official": {
        "name": "Vue 官方博客",
        "url": "https://vuejs.org/news",
        "category": "框架更新",
        "parser": "parse_vue_news"
    },
    "react_official": {
        "name": "React 官方博客",
        "url": "https://react.dev/blog",
        "category": "框架更新",
        "parser": "parse_react_news"
    },
    "vite_official": {
        "name": "Vite 官方博客",
        "url": "https://vitejs.dev/blog",
        "category": "生态工具",
        "parser": "parse_vite_news"
    },
    "github_trending": {
        "name": "GitHub Trending Frontend",
        "url": "https://github.com/trending/frontend?since=weekly",
        "category": "开源项目",
        "parser": "parse_github_trending"
    },
    "juejin_frontend": {
        "name": "掘金前端热门",
        "url": "https://juejin.cn/column/6896228171065718797",
        "category": "行业实践",
        "parser": "parse_juejin_news"
    }
}

# -------------------------- 工具函数 --------------------------
def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")
        return None

def parse_vue_news(soup):
    news_list = []
    if not soup:
        return news_list
    items = soup.select(".news-item")[:3]
    for item in items:
        title = item.select_one("h3").get_text(strip=True) if item.select_one("h3") else "无标题"
        link = "https://vuejs.org" + item.select_one("a")["href"] if item.select_one("a") else "#"
        desc = item.select_one(".news-desc").get_text(strip=True)[:150] + "..." if item.select_one(".news-desc") else "无简介"
        news_list.append({"title": title, "link": link, "desc": desc})
    return news_list

def parse_react_news(soup):
    news_list = []
    if not soup:
        return news_list
    items = soup.select(".css-1dbjc4n.r-1w6e6rj.r-13qz1uu")[:3]
    for item in items:
        title = item.select_one("h2").get_text(strip=True) if item.select_one("h2") else "无标题"
        link = "https://react.dev" + item.select_one("a")["href"] if item.select_one("a") else "#"
        desc = item.select_one("p").get_text(strip=True)[:150] + "..." if item.select_one("p") else "无简介"
        news_list.append({"title": title, "link": link, "desc": desc})
    return news_list

def parse_vite_news(soup):
    news_list = []
    if not soup:
        return news_list
    items = soup.select(".blog-post-card")[:3]
    for item in items:
        title = item.select_one("h3").get_text(strip=True) if item.select_one("h3") else "无标题"
        link = "https://vitejs.dev" + item.select_one("a")["href"] if item.select_one("a") else "#"
        desc = item.select_one("p").get_text(strip=True)[:150] + "..." if item.select_one("p") else "无简介"
        news_list.append({"title": title, "link": link, "desc": desc})
    return news_list

def parse_github_trending(soup):
    news_list = []
    if not soup:
        return news_list
    items = soup.select(".Box-row")[:5]
    for item in items:
        title = item.select_one("h3").get_text(strip=True).replace("\n", "").replace(" ", "") if item.select_one("h3") else "无标题"
        link = "https://github.com" + item.select_one("a")["href"] if item.select_one("a") else "#"
        stars = item.select_one(".octicon-star").next_sibling.get_text(strip=True) if item.select_one(".octicon-star") else "0"
        desc = item.select_one("p").get_text(strip=True)[:150] + "..." if item.select_one("p") else "无简介"
        news_list.append({"title": f"{title} ⭐{stars}", "link": link, "desc": desc})
    return news_list

def parse_juejin_news(soup):
    news_list = []
    if not soup:
        return news_list
    items = soup.select(".article-item")[:3]
    for item in items:
        title = item.select_one("h3").get_text(strip=True) if item.select_one("h3") else "无标题"
        link = "https://juejin.cn" + item.select_one("a")["href"] if item.select_one("a") else "#"
        desc = item.select_one(".abstract").get_text(strip=True)[:150] + "..." if item.select_one(".abstract") else "无简介"
        news_list.append({"title": title, "link": link, "desc": desc})
    return news_list

# -------------------------- 主逻辑：生成结构化内容 --------------------------
def generate_md_content():
    # 初始化分类
    categories = {
        "框架更新": [],
        "生态工具": [],
        "开源项目": [],
        "行业实践": []
    }

    # 爬取所有源的资讯
    for source_id, source_info in NEWS_SOURCES.items():
        soup = get_soup(source_info["url"])
        parser_func = globals()[source_info["parser"]]
        news = parser_func(soup)
        if news:
            categories[source_info["category"]].extend(news)

    # 构建Markdown内容
    md = f"""# 📅 {week_num} 前端技术周刊 · {week_str}
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 开源地址：[weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

> 每周一自动更新，精选前端领域「框架更新/生态工具/开源项目/行业实践」，帮你高效掌握前端趋势。

---

## 🚀 框架更新
"""
    for item in categories["框架更新"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"
    if not categories["框架更新"]:
        md += "本周暂无重大框架更新\n\n---\n"

    md += "## 🛠️ 生态工具\n"
    for item in categories["生态工具"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"
    if not categories["生态工具"]:
        md += "本周暂无重大工具更新\n\n---\n"

    md += "## 🌟 热门开源项目\n"
    for item in categories["开源项目"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"
    if not categories["开源项目"]:
        md += "本周暂无热门开源项目\n\n---\n"

    md += "## 💡 行业实践与深度文章\n"
    for item in categories["行业实践"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"
    if not categories["行业实践"]:
        md += "本周暂无精选文章\n\n---\n"

    # 引流与互动模块
    md += """## 📢 关于本项目
- 本仓库每周一 8:00 自动更新，所有资讯均来自官方/高价值社区，经过结构化整理；
- 如果你觉得内容有帮助，欢迎给个 ⭐ Star 支持，你的鼓励是持续更新的动力；
- 欢迎提交 Issue/PR 补充你发现的优质资讯，一起共建前端技术社区；
- 关注我，获取更多前端自动化与工程化实践分享。

> 「技术沉淀，开源共享」—— WednesdayCAT
"""
    return md

# -------------------------- 写入文件 --------------------------
if __name__ == "__main__":
    content = generate_md_content()
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 资讯文件已生成：{md_file_path}")