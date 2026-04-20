# 📚 weekly-frontend-news

> 每周一自动更新的前端技术周刊，帮你高效掌握前端趋势

[![Update](https://github.com/WednesdayCAT/weekly-frontend-news/actions/workflows/weekly-publish.yml/badge.svg)](https://github.com/WednesdayCAT/weekly-frontend-news/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ 项目亮点

- 🤖 **自动化生成**：GitHub Actions 定时跑，每周一 8:00 自动发布
- 📚 **结构化存储**：按年/周归档，支持索引查询
- 🔔 **多格式订阅**：RSS / JSON Feed / Atom 全支持
-  **共享访问**：GitHub Pages + 原始文件直链
- 📊 **数据统计**：元数据管理，周刊统计一目了然

---

## 📅 最近更新

| 期数 | 日期 | 重点内容 | 链接 |
|------|------|----------|------|
| 2026-17 | 04-27 | Vue3 组合式 API、Next.js SSR | [查看](archives/2026/week-17.md) |
| 2026-16 | 04-20 | WebSkill 开源、Vue 组件指南 | [查看](archives/2026/week-16.md) |

📚 **[完整存档索引](archives/README.md)**

---

## 🚀 快速使用

### 订阅周刊

| 方式 | 链接 |
|------|------|
| 📬 RSS | [rss.xml](rss.xml) |
| 📄 JSON Feed | [feed.json](feed.json) |
| ⚛️ Atom | [atom.xml](atom.xml) |

**订阅地址**（复制到 RSS 阅读器）：
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/rss.xml
```

### 本地运行

```bash
# 克隆项目
git clone https://github.com/WednesdayCAT/weekly-frontend-news.git
cd weekly-frontend-news

# 安装依赖
npm install

# 生成周刊
npm run generate

# 构建索引和 RSS
npm run index && npm run rss
```

---

## 📁 目录结构

```
weekly-frontend-news/
├── archives/              # 周刊存档
│   ├── index.json        # 索引文件
│   ├── README.md         # 存档列表
│   └── 2026/             # 按年份存储
│       └── week-17.md
├── scripts/               # 自动化脚本
│   ├── generate-weekly.js
│   ├── build-index.js
│   └── build-rss.js
├── template/              # 模板文件
├── rss.xml               # RSS 订阅
└── README.md
```

---

## 📌 内容模块

| 模块 | 说明 |
|------|------|
| 🚀 框架更新 | Vue/React/Angular/Next.js 等官方动态 |
| 🛠️ 生态工具 | Vite/Webpack/Tailwind 等工具更新 |
| 🌟 开源项目 | GitHub 高星前端项目推荐 |
| 🌐 Web 标准 | CSS/HTTP/浏览器新特性 |
| 💡 行业实践 | 大厂落地案例、优化方案 |

---

## 📤 共享方式

### 1. 直接访问
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/archives/2026/week-17.md
```

### 2. RSS 订阅
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/rss.xml
```

### 3. API 访问
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/archives/index.json
```

### 4. GitHub Pages
启用后访问：`https://WednesdayCAT.github.io/weekly-frontend-news/`

📖 **详细文档**：[docs/SHARING.md](docs/SHARING.md)

---

## 📊 统计信息

```bash
# 查看周刊统计
node scripts/metadata.js stats
```

---

## 🛠️ 开发命令

| 命令 | 说明 |
|------|------|
| `npm run generate` | 生成当周周刊 |
| `npm run index` | 构建周刊索引 |
| `npm run rss` | 生成 RSS 订阅源 |
| `npm run publish` | 完整发布流程 |

---

## 📢 关于我

- 前端组长，专注前端工程化与自动化实践
- 分享前端技术趋势、自动化工具与职业成长经验
- 欢迎关注我的 GitHub，一起进步！

---

##  License

MIT © [WednesdayCAT](https://github.com/WednesdayCAT)

---

> 技术沉淀，开源共享 — 每周一 8:00 准时更新

📬 **订阅**：[RSS](rss.xml) | [JSON](feed.json) | [Atom](atom.xml)  
📚 **存档**：[archives/README.md](archives/README.md)  
📖 **文档**：[docs/SHARING.md](docs/SHARING.md)
