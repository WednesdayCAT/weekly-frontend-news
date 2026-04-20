import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import re

# -------------------------- 1. 配置信息（可抽离到config.py）--------------------------
# 前端核心资讯爬取源（精选高价值、更新及时的源，避免垃圾信息）
NEWS_SOURCES = {
    "Vue官方": "https://vuejs.org/news",
    "React官方": "https://react.dev/blog",
    "Vite官方": "https://vitejs.dev/blog",
    "前端之巅": "https://juejin.cn/column/6896228171065718797",
    "掘金前端": "https://juejin.cn/tag/前端/newest",
    "GitHub Trending Frontend": "https://github.com/trending/frontend?since=weekly"
}
# 资讯保存目录
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
# 模板文件路径
TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "template", "news_template.md")
# 计算上周时间范围（周一到周日）
today = datetime.now()
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
week_str = f"{last_monday.strftime('%Y-%m-%d')}至{last_sunday.strftime('%Y-%m-%d')}"
week_num = f"{today.year}-{today.isocalendar()[1]-1}周"  # 年度周数
md_file_name = f"{week_num}（{last_monday.strftime('%m%d')}-{last_sunday.strftime('%m%d')}）.md"
md_file_path = os.path.join(DOCS_DIR, today.strftime('%Y'), md_file_name)

# -------------------------- 2. 工具函数：爬取+解析内容 --------------------------
def get_page_content(url, encoding="utf-8"):
    """爬取网页内容，返回BeautifulSoup对象"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 抛出HTTP错误
        response.encoding = encoding
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"爬取{url}失败：{e}")
        return None

def extract_news(soup, source_name):
    """根据不同源，提取资讯标题+链接+简介（可自定义解析规则）"""
    news_list = []
    if source_name == "Vue官方":
        # Vue官方新闻解析规则（示例）
        items = soup.select(".news-item")
        for item in items[:5]: # 取最新5条
            title = item.select_one("h3").get_text(strip=True) if item.select_one("h3") else "无标题"
            link = "https://vuejs.org" + item.select_one("a")["href"] if item.select_one("a") else "#"
            desc = item.select_one(".news-desc").get_text(strip=True)[:100] + "..." if item.select_one(".news-desc") else "无简介"
            news_list.append({"title": title, "link": link, "desc": desc, "source": source_name})
    # 可扩展其他源的解析规则（React/Vite/掘金等）
    return news_list

# -------------------------- 3. 核心逻辑：生成MD内容 --------------------------
def generate_md_content():
    """按模板生成MD资讯内容"""
    # 1. 爬取所有源的资讯
    all_news = {
        "框架更新": [],
        "生态工具": [],
        "性能优化": [],
        "行业实践": []
    }
    for source_name, url in NEWS_SOURCES.items():
        soup = get_page_content(url)
        if soup:
            news = extract_news(soup, source_name)
            # 按源分类到对应模块（可自定义分类规则）
            if source_name in ["Vue官方", "React官方", "Vite官方"]:
                all_news["框架更新"].extend(news)
            elif source_name == "GitHub Trending Frontend":
                all_news["生态工具"].extend(news)
            else:
                all_news["性能优化"].extend(news)

    # 2. 读取模板文件
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    # 3. 替换模板变量，生成最终内容
    md_content = template.replace("{{WEEK_STR}}", week_str)\
                         .replace("{{WEEK_NUM}}", week_num)\
                         .replace("{{UPDATE_TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # 拼接各模块资讯内容
    for module, news in all_news.items():
        module_content = ""
        for n in news:
            module_content += f"- **[{n['title']}]({n['link']})**\n  > {n['desc']} 【来源：{n['source']}】\n\n"
        md_content = md_content.replace(f"{{{{{module}}}}}", module_content if module_content else "本周暂无相关资讯")
    
    return md_content

# -------------------------- 4. 保存MD文件 --------------------------
def save_md_file(content):
    """保存生成的MD文件到指定目录"""
    # 创建年度目录（如果不存在）
    year_dir = os.path.join(DOCS_DIR, datetime.now().strftime('%Y'))
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)
    # 写入文件
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"资讯生成成功，保存路径：{md_file_path}")

# -------------------------- 主函数 --------------------------
if __name__ == "__main__":
    md_content = generate_md_content()
    save_md_file(md_content)