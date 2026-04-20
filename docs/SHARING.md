# 📦 周刊存储共享方案

本仓库提供完整的前端周刊存储和共享解决方案，支持多种访问和订阅方式。

---

##  目录结构

```
weekly-frontend-news/
├── archives/                    # 周刊存档目录
│   ├── index.json              # 周刊索引（JSON 格式）
│   ├── README.md               # 周刊索引（Markdown 格式）
│   ├── metadata.json           # 元数据管理
│   ├── 2026/                   # 按年份存储
│   │   └── week-16.md
│   │   └── week-17.md
│   └── 2025/
├── template/                    # 模板文件
│   └── weekly.hbs              # 周刊 Markdown 模板
├── scripts/                     # 自动化脚本
│   ├── generate-weekly.js      # 生成周刊
│   ├── build-index.js          # 构建索引
│   ├── build-rss.js            # 构建 RSS
│   └── metadata.js             # 元数据管理
├── rss.xml                      # RSS 订阅源
├── feed.json                    # JSON Feed
├── atom.xml                     # Atom 订阅源
└── README.md                    # 项目说明
```

---

## 🚀 快速开始

### 安装依赖
```bash
npm install
```

### 生成周刊
```bash
npm run generate    # 生成当周周刊
npm run index       # 构建周刊索引
npm run rss         # 生成 RSS 订阅源
```

### 完整流程
```bash
npm run publish     # 抓取 + 生成 + 索引+RSS
```

---

## 📤 共享方式

### 1. GitHub 直接访问

**周刊原文**：
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/archives/2026/week-17.md
```

**索引文件**：
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/archives/index.json
```

### 2. RSS 订阅

| 格式 | 链接 |
|------|------|
| RSS 2.0 | [rss.xml](https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/rss.xml) |
| JSON Feed | [feed.json](https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/feed.json) |
| Atom | [atom.xml](https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/atom.xml) |

**订阅地址示例**：
```
https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/rss.xml
```

### 3. GitHub Pages（推荐）

启用 GitHub Pages 后，可通过网页访问：

```
https://WednesdayCAT.github.io/weekly-frontend-news/
```

**配置步骤**：
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main / docs
4. Save

### 4. API 访问

通过索引 JSON 获取周刊列表：

```bash
curl https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/archives/index.json
```

**返回示例**：
```json
{
  "updatedAt": "2026-04-21T12:00:00.000Z",
  "totalWeeks": 17,
  "weeks": [
    {
      "year": 2026,
      "weekNum": 17,
      "title": "2026-17 周 前端技术周刊",
      "updatedAt": "2026-04-21",
      "path": "2026/week-17.md",
      "url": "https://raw.githubusercontent.com/..."
    }
  ]
}
```

---

## 📊 数据统计

查看周刊统计信息：

```bash
node scripts/metadata.js stats
```

**输出示例**：
```
📊 周刊统计:
   总期数：17
   总条目：85
   平均每周期：5 条
```

---

## 🔧 自定义配置

### 修改数据源

编辑 `scripts/fetch-news.js`，添加或修改资讯源：

```javascript
const SOURCES = [
  {
    name: '掘金前端',
    url: 'https://juejin.cn/frontend?sort=newest',
    selector: '.article-list'
  },
  // 添加更多源...
];
```

### 修改模板

编辑 `template/weekly.hbs` 自定义周刊格式。

### 修改发布频率

编辑 `.github/workflows/weekly-publish.yml`：

```yaml
on:
  schedule:
    - cron: '0 0 * * 1'  # 每周一 0:00 UTC
```

---

## 📝 最佳实践

### 1. 版本控制
- 所有周刊文件纳入 Git 管理
- 每次生成后自动提交推送

### 2. 数据备份
- 定期下载 `archives/` 目录本地备份
- 使用 GitHub Releases 标记重要版本

### 3. 内容审核
- 生成后人工审核内容质量
- 通过 PR 流程合并更新

### 4. 性能优化
- RSS 仅保留最近 20 期
- 索引文件按需加载

---

## 🤝 贡献指南

欢迎提交 Issue/PR 改进存储共享方案！

- 报告问题：[Issues](https://github.com/WednesdayCAT/weekly-frontend-news/issues)
- 功能建议：[Discussions](https://github.com/WednesdayCAT/weekly-frontend-news/discussions)

---

## 📄 License

MIT © [WednesdayCAT](https://github.com/WednesdayCAT)
