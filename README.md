# 📚 weekly-frontend-news

> 每周一自动更新的前端技术周刊，帮你高效掌握前端趋势

[![Auto Generate](https://github.com/WednesdayCAT/weekly-frontend-news/actions/workflows/auto-generate-weekly-frontend-news.yml/badge.svg)](https://github.com/WednesdayCAT/weekly-frontend-news/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 项目亮点

- 🤖 **自动化生成**：GitHub Actions 定时运行，每周一 8:00 (UTC+8) 自动发布
- 📚 **结构化存储**：按 `年/周` 归档，方便检索和回溯
- 🔒 **内容精选**：基于 GitHub API、RSS 订阅源自动抓取，过滤低价值信息
- 📦 **开源共享**：所有内容基于 MIT 协议开源，可自由复用

---

## 📅 最近更新

| 期数 | 日期 | 链接 |
|------|------|------|
| 2026-16周 | 04-14 ~ 04-20 | [查看](docs/2026/2026-16周%20前端技术周报.md) |

📚 **存档目录**：[`docs/`](docs/)

---

## 🚀 快速开始

### 在线阅读

直接访问仓库 [`docs/2026/`](docs/2026/) 目录查看最新周刊。

### 本地运行

```bash
# 克隆项目
git clone https://github.com/WednesdayCAT/weekly-frontend-news.git
cd weekly-frontend-news

# 安装 Python 依赖
pip install -r requirements.txt

# 生成当周周刊
python scripts/generate_weekly_news.py
```

---

## 📁 目录结构

```
weekly-frontend-news/
├── .github/
│   └── workflows/
│       └── auto-generate-weekly-frontend-news.yml   # GitHub Actions 自动化工作流
├── docs/                                              # 周刊文档存档
│   └── 2026/
│       └── 2026-16周 前端技术周报.md
├── scripts/
│   └── generate_weekly_news.py                        # 周刊生成脚本（Python）
├── requirements.txt                                   # Python 依赖
├── LICENSE                                            # MIT 开源协议
└── README.md                                          # 项目说明
```

---

## 📌 内容模块

每期周刊包含以下模块：

| 模块 | 说明 |
|------|------|
| 🚀 框架更新 | Vue / React / Angular 等主流框架官方动态 |
| 🛠️ 生态工具 | Vite / Webpack / TypeScript 等工具链更新 |
| 🌟 热门开源 | GitHub 高星前端项目推荐 |
| 💡 行业实践 | 前端工程化、性能优化、大厂技术方案 |

---

## 🛠️ 技术栈

- **Python 3.11** — 核心脚本语言
- **requests** — HTTP 请求
- **beautifulsoup4** — HTML/XML 解析
- **feedparser** — RSS/Atom 订阅源解析
- **GitHub Actions** — 自动化定时任务

---

## 📢 关于我

- 前端组长，专注前端工程化与自动化实践
- 分享前端技术趋势、自动化工具与职业成长经验
- 欢迎关注我的 GitHub，一起进步！

---

## 📄 License

MIT © [WednesdayCAT](https://github.com/WednesdayCAT)

---

> 技术沉淀，开源共享 — 每周一 8:00 准时更新
