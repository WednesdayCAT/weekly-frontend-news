#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端每周资讯自动生成脚本
基于 GitHub API、Hacker News API 和各大官方博客 RSS
"""

import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

# ================= 时间计算 =================
today = datetime.now()
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
week_num = f"{today.year}-{today.isocalendar()[1]-1}周"
week_str = f"{last_monday.strftime('%Y-%m-%d')} 至 {last_sunday.strftime('%Y-%m-%d')}"
md_file_name = f"{today.year}-{today.isocalendar()[1]-1}周（{last_monday.strftime('%m%d')}-{last_sunday.strftime('%m%d')}）.md"

# ================= 文件路径 =================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, "docs", str(today.year))
os.makedirs(docs_dir, exist_ok=True)
md_file_path = os.path.join(docs_dir, md_file_name)

# ================= 数据源 =================

def fetch_github_trending():
    """通过 GitHub API 获取本周热门前端项目"""
    print("📡 正在获取 GitHub 热门项目...")
    try:
        # 搜索最近一周创建的前端项目
        from datetime import datetime, timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"language:javascript OR language:typescript OR language:vue OR language:react created:>{week_ago}",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "weekly-frontend-news-bot"
        }
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        items = r.json().get("items", [])
        
        results = []
        for item in items[:5]:
            results.append({
                "title": f"{item['full_name']} ⭐{item['stargazers_count']}",
                "link": item["html_url"],
                "desc": item["description"][:150] + "..." if item.get("description") else "前端开源项目",
                "stars": item['stargazers_count'],
                "language": item.get('language', 'N/A')
            })
        
        print(f"✅ 获取到 {len(results)} 个热门项目")
        return results
    except Exception as e:
        print(f"❌ GitHub 热门项目获取失败: {e}")
        return []


def fetch_hacker_news():
    """从 Hacker News 获取前端相关讨论"""
    print("📡 正在获取 Hacker News 热门讨论...")
    try:
        # 获取 HN 的 top stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        r = requests.get(url, timeout=10)
        story_ids = r.json()[:20]  # 取前20个
        
        results = []
        frontend_keywords = ['javascript', 'typescript', 'react', 'vue', 'angular', 
                           'frontend', 'web', 'node', 'npm', 'webpack', 'vite']
        
        for story_id in story_ids[:15]:
            try:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_r = requests.get(story_url, timeout=5)
                story = story_r.json()
                
                title = story.get('title', '').lower()
                # 检查是否包含前端关键词
                if any(keyword in title for keyword in frontend_keywords):
                    results.append({
                        "title": story.get('title', '无标题'),
                        "link": story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        "desc": f"Hacker News 讨论 · {story.get('score', 0)} 分 · {story.get('descendants', 0)} 条评论",
                        "score": story.get('score', 0)
                    })
                    
                    if len(results) >= 4:
                        break
            except:
                continue
        
        print(f"✅ 获取到 {len(results)} 条 Hacker News 讨论")
        return results
    except Exception as e:
        print(f"❌ Hacker News 获取失败: {e}")
        return []


def fetch_devto_articles():
    """从 Dev.to 获取前端文章"""
    print("📡 正在获取 Dev.to 前端文章...")
    try:
        url = "https://dev.to/api/articles"
        params = {
            "tag": "javascript",
            "per_page": 5,
            "top": 1  # 本周热门文章
        }
        
        r = requests.get(url, params=params, timeout=10)
        articles = r.json()
        
        results = []
        for article in articles[:5]:
            results.append({
                "title": article.get('title', '无标题'),
                "link": f"https://dev.to/{article.get('path', '')}",
                "desc": f"作者: {article.get('user', {}).get('name', '匿名')} · {article.get('reading_time_minutes', 0)} 分钟阅读",
                "tags": article.get('tag_list', [])
            })
        
        print(f"✅ 获取到 {len(results)} 篇 Dev.to 文章")
        return results
    except Exception as e:
        print(f"❌ Dev.to 文章获取失败: {e}")
        return []


def fetch_recent_framework_updates():
    """模拟获取框架更新（实际项目应接入真实 RSS/API）"""
    print("📡 正在获取框架更新信息...")
    
    # 这里提供一个模板，实际使用时应接入真实的框架更新源
    # 例如：Vue GitHub releases, React changelog 等
    
    results = []
    
    # 示例：可以手动维护或者接入 GitHub Releases API
    frameworks = [
        {
            "name": "Vue.js",
            "url": "https://api.github.com/repos/vuejs/core/releases/latest"
        },
        {
            "name": "React",
            "url": "https://api.github.com/repos/facebook/react/releases/latest"
        },
        {
            "name": "Vite",
            "url": "https://api.github.com/repos/vitejs/vite/releases/latest"
        }
    ]
    
    for fw in frameworks:
        try:
            r = requests.get(fw['url'], timeout=10)
            release = r.json()
            
            if 'message' not in release:  # 不是错误响应
                pub_date = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
                # 只包含最近两周的更新
                two_weeks_ago = datetime.now() - timedelta(days=14)
                if pub_date > two_weeks_ago:
                    results.append({
                        "title": f"{fw['name']} {release['tag_name']} 发布",
                        "link": release['html_url'],
                        "desc": release.get('name', '')[:150] if release.get('name') else "框架版本更新",
                        "date": release['published_at'][:10]
                    })
        except Exception as e:
            print(f"  警告: {fw['name']} 更新获取失败: {e}")
            continue
    
    print(f"✅ 获取到 {len(results)} 个框架更新")
    return results


# ================= 内容生成 =================

def generate_markdown():
    """生成完整的 Markdown 内容"""
    print("\n🚀 开始生成前端周刊...")
    print(f"📅 周期: {week_num} ({week_str})\n")
    
    # 收集所有数据
    framework_updates = fetch_recent_framework_updates()
    github_trending = fetch_github_trending()
    hacker_news = fetch_hacker_news()
    devto_articles = fetch_devto_articles()
    
    # 如果没有获取到数据，提供默认内容
    if not framework_updates:
        framework_updates = [{
            "title": "暂无本周框架更新",
            "link": "#",
            "desc": "本周各大框架无重大版本发布，建议关注各框架的 GitHub Issues 了解最新动态。"
        }]
    
    # 合并 HN 和 Dev.to 作为行业实践
    industry_practice = hacker_news + devto_articles
    if not industry_practice:
        industry_practice = [{
            "title": "前端性能优化最佳实践",
            "link": "https://web.dev/articles/performance",
            "desc": "Google Web Dev 提供的性能优化指南，涵盖 Core Web Vitals 优化技巧"
        }]
    
    # 生成 Markdown
    md_content = f"""# 📅 {week_num} 前端技术周刊 · {week_str}

更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 开源地址：[weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

> 🤖 **全自动化生成**：基于 GitHub API、Hacker News API 和 Dev.to，不受网页结构变动影响，稳定每周一更新。

---

## 🚀 框架更新

"""
    
    for item in framework_updates:
        md_content += f"- **[{item['title']}]({item['link']})**\n"
        md_content += f"  > {item['desc']}\n\n"
    
    md_content += "---\n\n"
    md_content += "## 🛠️ 生态工具与热门项目\n\n"
    
    for item in github_trending:
        md_content += f"- **[{item['title']}]({item['link']})** `⭐{item.get('stars', 0)}` `语言: {item.get('language', 'N/A')}`\n"
        md_content += f"  > {item['desc']}\n\n"
    
    if not github_trending:
        md_content += "> 本周暂无特别热门的开源项目\n\n"
    
    md_content += "---\n\n"
    md_content += "## 💡 行业实践与深度文章\n\n"
    
    for item in industry_practice:
        md_content += f"- **[{item['title']}]({item['link']})**\n"
        md_content += f"  > {item['desc']}\n\n"
    
    md_content += """---

## 📢 关于本期周刊

- 🤖 **自动化生成**：内容基于各大 API 自动抓取，确保时效性和准确性
- 📅 **更新频率**：每周一 8:00 (UTC+8) 自动更新
- 🔧 **数据来源**：GitHub API、Hacker News API、Dev.to API
- 💬 **参与贡献**：欢迎提交 Issue/PR 补充内容或优化脚本

---

仓库地址：[WednesdayCAT/weekly-frontend-news](https://github.com/WednesdayCAT/weekly-frontend-news)

如果觉得有用，欢迎 **Star 🌟** 支持！
"""
    
    return md_content


# ================= 主函数 =================

if __name__ == "__main__":
    print("=" * 60)
    print("📰 前端每周资讯生成器")
    print("=" * 60)
    
    try:
        content = generate_markdown()
        
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"\n✅ 生成成功！")
        print(f"📄 文件路径: {md_file_path}")
        print(f"📊 文件大小: {os.path.getsize(md_file_path) / 1024:.2f} KB")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
