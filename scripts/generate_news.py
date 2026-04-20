import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

# ================= 配置 =================
today = datetime.now()
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
week_num = f"{today.year}-{today.isocalendar()[1]-1}周"
week_str = f"{last_monday.strftime('%Y-%m-%d')} 至 {last_sunday.strftime('%Y-%m-%d')}"
md_file_name = f"{week_num}（{last_monday.strftime('%m%d')}-{last_sunday.strftime('%m%d')}）.md"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, "docs", str(today.year))
os.makedirs(docs_dir, exist_ok=True)
md_file_path = os.path.join(docs_dir, md_file_name)

# ================= 稳定数据源（官方API/RSS） =================
def fetch_github_trending():
    """GitHub Trending 官方API（稳定）"""
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "language:javascript language:typescript",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        r = requests.get(url, timeout=10)
        items = r.json().get("items", [])
        return [
            {
                "title": f"{item['name']} ⭐{item['stargazers_count']}",
                "link": item["html_url"],
                "desc": item["description"][:120] + "..." if item["description"] else "无描述"
            }
            for item in items
        ]
    except Exception as e:
        print(f"GitHub trending 爬取失败: {e}")
        return []

def fetch_official_blogs():
    """官方博客（使用RSS避免解析HTML）"""
    feeds = {
        "Vue": "https://blog.vuejs.org/feed.xml",
        "React": "https://react.dev/feed.xml",
        "Vite": "https://vitejs.dev/feed.xml"
    }
    results = []
    for source, url in feeds.items():
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "xml")
            items = soup.find_all("item", limit=2)
            for item in items:
                title = item.find("title").text if item.find("title") else "无标题"
                link = item.find("link").text if item.find("link") else "#"
                pub_date = item.find("pubDate").text if item.find("pubDate") else ""
                # 过滤上周内容
                pub_time = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                if last_monday <= pub_time <= last_sunday:
                    results.append({
                        "title": title,
                        "link": link,
                        "desc": f"来自 {source} 官方博客",
                        "category": "框架更新" if source in ["Vue", "React"] else "生态工具"
                    })
        except Exception as e:
            print(f"{source} 博客爬取失败: {e}")
    return results

def fetch_juejin_rss():
    """掘金前端RSS（免解析）"""
    try:
        url = "https://juejin.cn/rss/column/6896228171065718797"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "xml")
        items = soup.find_all("item", limit=4)
        return [
            {
                "title": item.find("title").text,
                "link": item.find("link").text,
                "desc": "掘金前端精选文章",
                "category": "行业实践"
            }
            for item in items
        ]
    except Exception as e:
        print(f"掘金爬取失败: {e}")
        return []

# ================= 主逻辑 =================
def generate_md():
    data = {
        "框架更新": [],
        "生态工具": [],
        "热门开源项目": [],
        "行业实践与深度文章": []
    }

    # 1. 官方博客 (Vue/React/Vite)
    blogs = fetch_official_blogs()
    for item in blogs:
        data[item["category"]].append(item)

    # 2. GitHub Trending
    data["热门开源项目"] = fetch_github_trending()

    # 3. 掘金文章
    data["行业实践与深度文章"] = fetch_juejin_rss()

    # 兜底
    for k in data:
        if not data[k]:
            data[k] = [{"title": "本周暂无重大更新", "link": "#", "desc": "无"}]

    # 生成Markdown
    md = f"""# 📅 {week_num} 前端技术周刊 · {week_str}
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 开源地址：[weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

> 🤖 **全自动化生成**：基于GitHub API与官方RSS，不受网页结构变动影响，稳定每周一更新。

---

## 🚀 框架更新
"""
    for item in data["框架更新"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"

    md += "## 🛠️ 生态工具\n"
    for item in data["生态工具"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"

    md += "## 🌟 热门开源项目\n"
    for item in data["热门开源项目"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"

    md += "## 💡 行业实践与深度文章\n"
    for item in data["行业实践与深度文章"]:
        md += f"- **[{item['title']}]({item['link']})**\n  > {item['desc']}\n\n"

    md += """---
## 📢 支持我
如果这份周刊对您有帮助，欢迎 **Star 🌟** 鼓励，或提交 Issue/PR 补充内容，一起共建前端社区！

仓库地址：[WednesdayCAT/weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)
"""
    return md

# ================= 写入 =================
if __name__ == "__main__":
    content = generate_md()
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 生成成功: {md_file_path}")
