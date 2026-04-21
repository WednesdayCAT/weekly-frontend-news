import os
import re
import requests
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ===================== 全局配置（贴合Skill规则）=====================
# 权威资讯源（按优先级排序，可直接扩展）
FEED_SOURCES = [
    # 框架官方（Skill优先级1）
    {"name": "Vue官方", "url": "https://vuejs.org/feed.xml", "category": "框架与生态", "type": "rss"},
    {"name": "React官方", "url": "https://react.dev/feed.xml", "category": "框架与生态", "type": "rss"},
    {"name": "Vite官方", "url": "https://vitejs.dev/feed.xml", "category": "框架与生态", "type": "rss"},
    # 工程化工具（Skill优先级2）
    {"name": "MDN技术博客", "url": "https://developer.mozilla.org/zh-CN/feed/blog.xml", "category": "工程化与工具链", "type": "rss"},
    {"name": "GitHub Trending前端", "url": "https://github.com/trending/frontend?since=weekly", "category": "开源项目", "type": "html"},
    # 行业资讯（Skill优先级6/7）
    {"name": "前端之巅", "url": "https://rsshub.app/frontend-trends", "category": "行业与安全", "type": "rss"},
    {"name": "掘金前端", "url": "https://rsshub.app/juejin/frontend", "category": "综合资讯", "type": "rss"},
    {"name": "Chrome开发者", "url": "https://developer.chrome.com/feeds/blog.xml", "category": "标准与跨端", "type": "rss"},
    {"name": "UniApp官方", "url": "https://uniapp.dcloud.io/feed.xml", "category": "标准与跨端", "type": "rss"},
    {"name": "TanStack官方", "url": "https://tanstack.com/feed.xml", "category": "开源项目", "type": "rss"},
    {"name": "Three.js官方", "url": "https://threejs.org/feed.xml", "category": "开源项目", "type": "rss"},
    {"name": "InfoQ前端", "url": "https://www.infoq.cn/rss/news_type/frontend.rss", "category": "行业与安全", "type": "rss"},
]
# 前端核心关键词（过滤非相关内容）
CORE_KEYWORDS = ["vue", "react", "vite", "rollup", "webpack", "css", "html", "js", "ts", "typescript",
                 "跨端", "微前端", "uniapp", "taro", "flutter", "web标准", "浏览器", "ai", "llm",
                 "组件库", "开源", "工程化", "性能优化", "安全合规", "无障碍", "github", "release"]
# 过滤无实质内容的关键词
FILTER_KEYWORDS = ["教程", "入门", "面试", "刷题", "福利", "招聘", "广告", "抽奖"]
# 请求头（避免被反爬）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# ===================== 工具函数：时间计算（核心）=====================
def get_last_week_info():
    """获取上周时间范围、年份、周数（贴合Skill时间规则）"""
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)  # 上周一
    last_sunday = last_monday + timedelta(days=6)              # 上周日
    date_range = f"{last_monday.strftime('%Y年%m月%d日')}-{last_sunday.strftime('%m月%d日')}"
    year = last_monday.strftime("%Y")
    week_num = f"{year}-{today.isocalendar()[1] - 1}周"
    # 时间戳（用于过滤资讯发布时间）
    start_ts = int(last_monday.timestamp())
    end_ts = int(last_sunday.timestamp())
    return {
        "date_range": date_range,
        "year": year,
        "week_num": week_num,
        "start_ts": start_ts,
        "end_ts": end_ts,
        "last_monday": last_monday,
        "last_sunday": last_sunday
    }

# ===================== 工具函数：资讯抓取 =====================
def fetch_rss_feed(source, last_week):
    """抓取RSS源资讯"""
    items = []
    try:
        feed = feedparser.parse(source["url"], request_headers=HEADERS)
        for entry in feed.entries[:10]:  # 限制条数，避免冗余
            # 解析发布时间
            pub_ts = 0
            if hasattr(entry, "published_parsed"):
                pub_ts = int(datetime(*entry.published_parsed[:6]).timestamp())
            elif hasattr(entry, "updated_parsed"):
                pub_ts = int(datetime(*entry.updated_parsed[:6]).timestamp())
            # 过滤时间范围
            if not (last_week["start_ts"] <= pub_ts <= last_week["end_ts"]):
                continue
            # 提取核心信息
            title = entry.title.strip() if hasattr(entry, "title") else ""
            link = entry.link.strip() if hasattr(entry, "link") else ""
            summary = entry.summary.strip() if hasattr(entry, "summary") else ""
            items.append({"title": title, "link": link, "summary": summary, "source": source})
    except Exception as e:
        print(f"⚠️  抓取RSS源{source['name']}失败：{str(e)[:50]}")
    return items

def fetch_github_trending(source, last_week):
    """抓取GitHub Trending前端周榜"""
    items = []
    try:
        res = requests.get(source["url"], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        repos = soup.select("div.Box-row")[:5]  # 取前5个热门项目
        for repo in repos:
            # 提取项目名称和链接
            name_elem = repo.select_one("h2.h3 a")
            if not name_elem:
                continue
            title = name_elem.get_text(strip=True).replace("\n", " ")
            link = urljoin("https://github.com", name_elem["href"])
            # 提取描述
            desc_elem = repo.select_one("p.col-9")
            summary = desc_elem.get_text(strip=True) if desc_elem else "GitHub热门前端开源项目"
            items.append({"title": title, "link": link, "summary": summary, "source": source})
    except Exception as e:
        print(f"⚠️  抓取GitHub Trending失败：{str(e)[:50]}")
    return items

def fetch_all_news(last_week):
    """抓取所有源资讯并初步过滤"""
    all_items = []
    for source in FEED_SOURCES:
        if source["type"] == "rss":
            all_items.extend(fetch_rss_feed(source, last_week))
        elif source["type"] == "html" and "github" in source["url"]:
            all_items.extend(fetch_github_trending(source, last_week))
    # 初步过滤：非前端内容、无标题/链接、广告内容
    filtered = []
    seen_links = set()  # 去重（按链接）
    for item in all_items:
        if not item["title"] or not item["link"] or item["link"] in seen_links:
            continue
        # 转小写方便匹配
        text = (item["title"] + " " + item["summary"]).lower()
        # 过滤非核心内容、广告内容
        if any(kw in text for kw in FILTER_KEYWORDS):
            continue
        if any(kw in text for kw in CORE_KEYWORDS):
            seen_links.add(item["link"])
            filtered.append(item)
    return filtered

# ===================== 工具函数：内容处理（贴合Skill规则）=====================
def extract_keyword(item):
    """提取2-4字关键词（Skill强制要求）"""
    text = (item["title"] + " " + item["summary"]).lower()
    # 按优先级匹配关键词
    kw_map = {
        "vue": "Vue", "react": "React", "vite": "Vite",
        "css": "CSS", "html": "Web标准", "js": "JS",
        "跨端": "跨端", "uniapp": "UniApp", "taro": "Taro",
        "ai": "AI开发", "llm": "AI开发",
        "开源": "开源", "github": "开源",
        "性能": "性能优化", "优化": "性能优化",
        "安全": "安全合规", "合规": "安全合规",
        "浏览器": "浏览器", "chrome": "Chrome"
    }
    for k, v in kw_map.items():
        if k in text:
            return v
    return "前端动态"

def classify_content(item):
    """按Skill规则分类（优先级：框架>工具>标准>行业>开源）"""
    # 优先使用源定义的分类，再动态匹配
    source_cat = item["source"]["category"]
    if source_cat != "综合资讯":
        return source_cat
    # 综合资讯动态分类
    text = (item["title"] + " " + item["summary"]).lower()
    if any(kw in text for kw in ["vue", "react", "vite", "rollup", "webpack"]):
        return "框架与生态"
    elif any(kw in text for kw in ["css", "html", "js", "ts", "工程化", "构建"]):
        return "工程化与工具链"
    elif any(kw in text for kw in ["浏览器", "web标准", "跨端", "uniapp", "taro"]):
        return "标准与跨端"
    elif any(kw in text for kw in ["安全", "合规", "趋势", "大厂", "行业"]):
        return "行业与安全"
    else:
        return "开源项目"

def simplify_content(title, summary):
    """精简内容（≤80字，保留核心更新+实际影响，Skill要求）"""
    # 清理HTML标签、多余空格、换行
    clean_sum = re.sub(r'<.*?>|\s+|\\n|\\r', ' ', summary).strip()
    # 合并标题和摘要，提取核心
    content = f"{title}：{clean_sum}"
    # 过滤无意义内容，保留核心动作（更新、发布、重构、优化、新增、修复）
    core_actions = re.findall(r'发布|更新|重构|优化|新增|修复|适配|落地|支持', content)
    if core_actions:
        # 保留核心动作及后续内容
        action_idx = content.find(core_actions[0])
        content = content[action_idx:] if action_idx != -1 else content
    # 限制长度，避免冗余
    return content[:77] + "..." if len(content) > 80 else content

# ===================== 核心函数：生成MD周报 =====================
def generate_weekly_md(last_week, news_items):
    """生成符合Skill规则的MD周报"""
    # 分类整理资讯
    categories = ["框架与生态", "工程化与工具链", "标准与跨端", "行业与安全", "开源项目"]
    grouped = {cat: [] for cat in categories}
    for item in news_items:
        cat = classify_content(item)
        if cat in grouped:
            grouped[cat].append({
                "keyword": extract_keyword(item),
                "title": item["title"],
                "content": simplify_content(item["title"], item["summary"]),
                "link": item["link"],
                "source_name": item["source"]["name"]
            })
    # 生成MD内容
    md_lines = [
        f"# {last_week['week_num']} 前端技术周报（{last_week['date_range']}）",
        f"更新时间：{datetime.now().strftime('%Y年%m月%d日')} | 开源地址：[weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)",
        "",
        "> 每周一自动生成，精选前端领域核心动态，严格遵循skill/weekly_frontend_news_auto_github.md规则，每条含权威链接与来源。",
        "---",
        ""
    ]
    # 遍历分类生成内容
    has_content = False
    for cat in categories:
        items = grouped[cat]
        if not items:
            continue
        has_content = True
        md_lines.append(f"## {cat}")
        md_lines.append("")
        for item in items[:3]:  # 每个分类最多3条，避免内容过长
            md_lines.append(f"- **「{item['keyword']}」**：[{item['title']}]({item['link']})")
            md_lines.append(f"  {item['content']}")
            md_lines.append(f"  来源：[{item['source_name']}]({item['link']})")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    # 无有效资讯时兜底
    if not has_content:
        md_lines.append(f"### {last_week['date_range'].split('-')[0][5:]}暂无前端领域核心动态")
        md_lines.append("")
    # 结尾说明（贴合Skill）
    md_lines.extend([
        "### 关于本项目",
        "- 本周报由GitHub Actions全自动生成，基于12个前端权威信息源抓取真实动态；",
        "- 严格过滤非核心内容，仅保留官方发布、实质更新、可落地的前端资讯；",
        "- 如果你觉得内容有帮助，欢迎给个⭐Star支持，也可提交Issue/PR补充优质资讯；",
        "- 仓库地址：[WednesdayCAT/weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)",
        "",
        "> 技术沉淀，开源共享 — WednesdayCAT"
    ])
    return "\n".join(md_lines)

# ===================== 主函数：执行全流程 =====================
if __name__ == "__main__":
    print("🔧 开始执行上周前端周报自动化生成流程...")
    # 1. 获取上周时间信息
    last_week = get_last_week_info()
    print(f"📅 目标时间范围：{last_week['date_range']}")
    print(f"📌 生成周数：{last_week['week_num']}")
    # 2. 抓取并过滤真实资讯
    news_items = fetch_all_news(last_week)
    print(f"📥 抓取并过滤后有效资讯数：{len(news_items)}")
    # 3. 生成MD内容
    md_content = generate_weekly_md(last_week, news_items)
    # 4. 保存文件（按年份分目录，Skill指定路径）
    save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", last_week["year"])
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{last_week['week_num']} 前端技术周报.md")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    # 5. 输出结果
    print(f"✅ 周报生成成功！文件路径：{save_path}")
    print(f"📦 文件大小：{os.path.getsize(save_path)} 字节")
    print("🔚 自动化生成流程执行完成！")