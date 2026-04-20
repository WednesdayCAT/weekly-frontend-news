#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含：爬取源、内容模板、仓库信息等配置
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 输出目录
OUTPUT_DIR = BASE_DIR / 'docs'

# 模板文件
TEMPLATE_FILE = BASE_DIR / 'template' / 'news_template.md'

# 爬取源配置
NEWS_SOURCES = [
    {
        'name': 'GitHub Trending',
        'url': 'https://github.com/trending',
        'type': 'trending',
        'enabled': True
    },
    {
        'name': 'Hacker News',
        'url': 'https://news.ycombinator.com/',
        'type': 'news',
        'enabled': True
    },
    {
        'name': 'Reddit Frontend',
        'url': 'https://www.reddit.com/r/Frontend/',
        'type': 'community',
        'enabled': True
    },
    {
        'name': 'CSS Tricks',
        'url': 'https://css-tricks.com/',
        'type': 'article',
        'enabled': True
    },
    {
        'name': 'Smashing Magazine',
        'url': 'https://www.smashingmagazine.com/',
        'type': 'article',
        'enabled': True
    }
]

# 爬虫配置
CRAWLER_CONFIG = {
    'timeout': 30,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'max_retries': 3,
    'delay_between_requests': 2  # 请求间隔（秒）
}

# 内容分类
CONTENT_CATEGORIES = {
    'framework_updates': '框架更新',
    'performance': '性能优化',
    'tools': '工具发布',
    'community': '社区动态',
    'articles': '优质文章'
}

# GitHub 仓库信息
REPO_INFO = {
    'owner': 'david',
    'repo': 'https://github.com/WednesdayCAT/weekly-frontend-news',
    'branch': 'main'
}
