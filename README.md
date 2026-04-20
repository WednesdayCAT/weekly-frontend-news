# 前端每周资讯

## 项目简介

前端每周资讯自动采集和生成系统，定期收集前端领域的最新动态、框架更新、工具发布等内容，自动生成结构化的 Markdown 文档。

## 使用说明

### 快速开始

1. 安装依赖：
```bash
cd scripts
pip install -r requirements.txt
```

2. 配置爬虫源：
编辑 `scripts/config.py`，设置需要爬取的网站和参数。

3. 生成资讯：
```bash
python scripts/generate_news.py
```

### 自动执行

本项目配置了 GitHub Actions，每周一 8:00 自动执行资讯生成。

## 目录结构

```
weekly-frontend-news/
├── docs/                    # 资讯主目录（按「年-周」命名，方便检索）
│   ├── 2026/
│   │   ├── 2026-16周（0414-0420）.md
│   │   ├── 2026-17周（0421-0427）.md
│   │   └── README.md        # 年度资讯汇总，带超链接索引
│   └── README.md            # 仓库首页，含简介、更新规则、目录索引
├── scripts/                 # 自动化脚本目录
│   ├── generate_news.py     # 核心：资讯爬取+内容生成+MD格式化的脚本
│   ├── config.py            # 配置文件：爬取源、内容模板、仓库信息
│   └── requirements.txt     # 脚本依赖包
├── .github/
│   └── workflows/           # GitHub Actions 定时任务配置
│       └── auto-generate-news.yml  # 每周一8:00自动执行的工作流
├── template/                # MD内容模板，统一格式（避免每次生成样式混乱）
│   └── news_template.md     # 资讯简报固定模板（框架更新/性能优化等模块）
├── LICENSE                  # 开源协议，建议用 MIT（宽松，方便他人复用）
└── README.md                # 仓库根目录README，含项目介绍、使用说明、贡献指南
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License