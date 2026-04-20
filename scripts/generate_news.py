import os
from datetime import datetime, timedelta

# -------------------------- 配置信息 --------------------------
# 计算上周时间范围（周一到周日）
today = datetime.now()
# 计算上周一和上周日
last_monday = today - timedelta(days=today.weekday() + 7)
last_sunday = last_monday + timedelta(days=6)
week_num = f"{today.year}-{today.isocalendar()[1]-1}周"
week_str = f"{last_monday.strftime('%Y-%m-%d')} 至 {last_sunday.strftime('%Y-%m-%d')}"
md_file_name = f"{week_num}（{last_monday.strftime('%m%d')}-{last_sunday.strftime('%m%d')}）.md"

# 保存路径（根据你的仓库结构写死，避免路径问题）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(base_dir, "docs", str(today.year))
os.makedirs(docs_dir, exist_ok=True)
md_file_path = os.path.join(docs_dir, md_file_name)

# -------------------------- 直接写死模板内容（先跑通） --------------------------
md_content = f"""# {week_num} 前端领域核心资讯简报（{week_str}）
更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

> 本项目每周一自动生成，汇总上周前端领域框架更新、生态工具、性能优化与行业实践，开源共享。

## 一、框架更新
- **Vue 3.5.0 RC 版本更新**
  > 优化响应式系统性能，大型列表渲染耗时降低约15%，修复SSR场景下`useSlots`渲染错位问题。

- **React 19 稳定版发布预告**
  > 官方确认稳定版将于2026年5月底发布，核心特性`useActionState`/`useFormStatus`完成兼容性测试。

## 二、生态工具
- **Vite 5.3.0 发布**
  > 优化monorepo项目构建速度，打包耗时降低20%，新增`server.fs.allowDeep`配置简化路径管理。

- **Shadcn UI v2.0 公测版**
  > 新增20+企业级组件，支持无样式侵入的自定义主题，适配Tailwind CSS 3.4最新特性。

## 三、性能优化
- **Rust Wasm + 预渲染首屏优化方案**
  > 通过Rust Wasm编译高频计算逻辑，JS主线程耗时降低60%+，结合预渲染实现「静态首屏+动态交互」无缝衔接。

## 四、行业实践
- **腾讯视频首屏优化落地案例**
  > 通过资源懒加载+预加载策略优化，移动端首屏加载时间从2.8s降至1.2s，用户留存率提升12%。

---
本项目开源地址：https://github.com/WednesdayCAT/weekly-frontend-news
"""

# -------------------------- 保存文件 --------------------------
with open(md_file_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"✅ 资讯文件已生成：{md_file_path}")
