import os
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

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

# ================= 通用请求工具 =================
def get_soup(url, verify=False):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15, verify=verify)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"❌ 爬取失败：{url} -> {e}")
        return None

# ================= 各平台专用解析器 =================
def parse_vue_blog(soup):
    items = soup.select(".news-item")[:3]
    news = []
    for item in items:
        title_elem = item.select_one("h3")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link_elem = item.select_one("a")
        if not link_elem:
            continue
        href = link_elem.get("href", "")
        if not href.startswith("http"):
            href = "https://blog.vuejs.org" + href
        desc_elem = item.select_one(".news-desc")
        desc = desc_elem.get_text(strip=True)[:150] + "..." if desc_elem else "无简介"
        news.append({
            "title": title,
            "link": href,
            "desc": desc
        })
    return news

def parse_react_blog(soup):
    items = soup.select(".css-1dbjc4n.r-1w6e6rj.r-13qz1uu")[:3]
    news = []
    for item in items:
        title_elem = item.select_one("h2")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link_elem = item.select_one("a")
        if not link_elem:
            continue
        href = link_elem.get("href", "")
        if not href.startswith("http"):
            href = "https://react.dev" + href
        desc_elem = item.select_one("p")
        desc = desc_elem.get_text(strip=True)[:150] + "..." if desc_elem else "无简介"
        news.append({
            "title": title,
            "link": href,
            "desc": desc
        })
    return news

def parse_vite_blog(soup):
    items = soup.select(".blog-post-card")[:3]
    news = []
    for item in items:
        title_elem = item.select_one("h3")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link_elem = item.select_one("a")
        if not link_elem:
            continue
        href = link_elem.get("href", "")
        if not href.startswith("http"):
            href = "https://vitejs.dev" + href
        desc_elem = item.select_one("p")
        desc = desc_elem.get_text(strip=True)[:150] + "..." if desc_elem else "无简介"
        news.append({
            "title": title,
            "link": href,
            "desc": desc
        })
    return news

def parse_github_trending(soup):
    items = soup.select(".Box-row")[:5]
    news = []
    for item in items:
        title_elem = item.select_one("h3")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True).replace("\n", "").replace(" ", "")
        link_elem = title_elem.select_one("a")
        if not link_elem:
            continue
        href = link_elem.get("href", "")
        if not href.startswith("http"):
            href = "https://github.com" + href
        star_elem = item.select_one(".octicon-star + span")
        star_text = star_elem.get_text(strip=True) if star_elem else "0"
        desc_elem = item.select_one("p")
        desc = desc_elem.get_text(strip=True)[:120] + "..." if desc_elem else "无描述"
        news.append({
            "title": f"{title} ⭐{star_text}",
            "link": href,
            "desc": desc
        })
    return news

def parse_juejin_collect(soup):
    items = soup.select(".article-item")[:4]
    news = []
    for item in items:
        title_elem = item.select_one("h3")
        if not title_elem:
            continue
        title = title_elem.get_text(strip=True)
        link_elem = item.select_one("a")
        if not link_elem:
            continue
        href = link_elem.get("href", "")
        if not href.startswith("http"):
            href = "https://juejin.cn" + href
        desc_elem = item.select_one(".abstract")
        desc = desc_elem.get_text(strip=True)[:120] + "..." if desc_elem else "无摘要"
        news.append({
            "title": title,
            "link": href,
            "desc": desc
        })
    return news

# ================= 主逻辑 =================
def generate_md():
    data = {
        "框架更新": [],
        "生态工具": [],
        "热门开源项目": [],
        "行业实践与深度文章": []
    }

    # 1. Vue 官方博客
    s = get_soup("https://blog.vuejs.org/")
    if s:
        data["框架更新"].extend(parse_vue_blog(s))

    # 2. React 官方博客
    s = get_soup("https://react.dev/blog")
    if s:
        data["框架更新"].extend(parse_react_blog(s))

    # 3. Vite 官方博客
    s = get_soup("https://vitejs.dev/blog")
    if s:
        data["生态工具"].extend(parse_vite_blog(s))

    # 4. GitHub Trending
    s = get_soup("https://github.com/trending/frontend?since=weekly")
    if s:
        data["热门开源项目"].extend(parse_github_trending(s))

    # 5. 掘金前端精选
    s = get_soup("https://juejin.cn/column/6896228171065718797")
    if s:
        data["行业实践与深度文章"].extend(parse_juejin_collect(s))

    # 兜底：如果没有数据，填充默认内容
    for k in data:
        if not data[k]:
            data[k] = [{"title": "本周暂无重大更新", "link": "#", "desc": "无"}]

    # 生成 Markdown
    md = f"""# 📅 {week_num} 前端技术周刊 · {week_str}
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 开源地址：[weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

> 🤖 每周一自动更新，基于 GitHub Actions 自动爬取与生成，精选前端框架、工具、开源项目与行业实践。

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

    # 引流模块
    md += f"""---

## 📢 欢迎关注 & Star
本项目每周一 8:00 自动更新，持续沉淀前端前沿资讯。
如果你觉得这份周刊有价值，欢迎 **Star 支持**，也欢迎提交 Issue/PR 补充你发现的优质内容，一起共建前端社区。

仓库地址：
👉 [https://github.com/WednesdayCAT/weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

---
📝 由 WednesdayCAT 前端团队自动化生成
"""
    return md

# ================= 写入文件 =================
if __name__ == "__main__":
    content = generate_md()
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 生成成功：{md_file_path}")
