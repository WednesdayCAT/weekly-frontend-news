// 生成周刊 Markdown
import fs from 'fs';
import path from 'path';
import Handlebars from 'handlebars';
import { addWeekMetadata } from './metadata.js';

function getWeekInfo() {
  const now = new Date();
  const oneJan = new Date(now.getFullYear(), 0, 1);
  const weekNum = Math.ceil((((now - oneJan) / 86400000) + oneJan.getDay() + 1) / 7);
  
  // 上周一和上周日
  const lastWeekStart = new Date(now);
  lastWeekStart.setDate(now.getDate() - now.getDay() - 6);
  const lastWeekEnd = new Date(lastWeekStart);
  lastWeekEnd.setDate(lastWeekStart.getDate() + 6);
  
  return {
    year: now.getFullYear(),
    weekNum: weekNum - 1,
    startDate: lastWeekStart.toISOString().split('T')[0].slice(5),
    endDate: lastWeekEnd.toISOString().split('T')[0].slice(5),
    updateDate: now.toISOString().split('T')[0]
  };
}

function generateWeekly() {
  const weekInfo = getWeekInfo();
  
  // 模拟数据（实际应从抓取脚本获取）
  const data = {
    year: weekInfo.year,
    weekNum: weekInfo.weekNum,
    startDate: weekInfo.startDate,
    endDate: weekInfo.endDate,
    updateDate: weekInfo.updateDate,
    frameworkUpdates: [
      {
        name: 'Vue.js 3.x',
        summary: '混入 mixins 与过滤器 filter 在 Vue2/Vue3 中的差异详解',
        description: 'Vue2 多使用 mixins 进行代码复用，Vue3 已移除 filter 过滤器，推荐使用组合式 API 替代。',
        source: '掘金',
        link: 'https://juejin.cn/frontend'
      },
      {
        name: 'Next.js App Router',
        summary: 'SSR/CSR、路由模型、缓存策略与 Server Action 基础速查',
        description: '系统梳理 Next.js 核心概念，包含最小示例快速上手，适合 React 开发者从 0 到 1 掌握服务端渲染实践。',
        source: '掘金',
        link: 'https://juejin.cn/frontend'
      }
    ],
    tools: [
      {
        name: 'JavaScript 颜色处理库',
        summary: '零依赖、链式调用、可变对象，重新设计颜色处理体验',
        description: '解决现有方案 API 反直觉、体积臃肿问题，提供轻量级颜色处理方案。',
        source: '掘金',
        link: 'https://juejin.cn/frontend'
      }
    ],
    projects: [
      {
        name: 'WebSkill',
        stars: '173+',
        summary: '运行在浏览器的 Agent 技能，OpenTiny 社区开源',
        description: '本文将基于这一架构，深入探讨 WebSkill 扮演的核心角色、独特价值、企业级应用场景。',
        source: '掘金',
        link: 'https://juejin.cn/post/7630681198802501695'
      }
    ],
    standards: [
      {
        name: 'W3C Window Splitter Pattern',
        summary: '基于规范的无障碍面板分割器，键盘友好交互设计',
        description: '教你用方向键和 Enter 键打造无障碍面板分割器，让键盘用户也能自由调整布局。',
        source: '掘金',
        link: 'https://juejin.cn/post/7630450023369850907'
      }
    ],
    articles: [
      {
        title: '首屏性能优化',
        summary: '6 个实战技巧让页面"秒开"，从网络请求到渲染全流程优化',
        description: '用户打开网站 3 秒白屏就会离开，本文从网络请求、资源加载、渲染优化等 6 个维度提供可落地的提速方案。',
        source: '掘金',
        link: 'https://juejin.cn/post/7630689270854926345'
      }
    ]
  };
  
  // 读取模板
  const templatePath = path.join(process.cwd(), 'template', 'weekly.hbs');
  const templateContent = fs.readFileSync(templatePath, 'utf-8');
  const template = Handlebars.compile(templateContent);
  const markdown = template(data);
  
  // 保存文件
  const archivesDir = path.join(process.cwd(), 'archives', weekInfo.year.toString());
  if (!fs.existsSync(archivesDir)) {
    fs.mkdirSync(archivesDir, { recursive: true });
  }
  
  const outputPath = path.join(archivesDir, `week-${weekInfo.weekNum}.md`);
  fs.writeFileSync(outputPath, markdown);
  
  console.log(`✅ 周刊已生成：${outputPath}`);
  
  // 更新元数据
  addWeekMetadata({
    year: weekInfo.year,
    weekNum: weekInfo.weekNum,
    frameworkUpdates: data.frameworkUpdates.length,
    tools: data.tools.length,
    projects: data.projects.length,
    standards: data.standards.length,
    articles: data.articles.length
  });
  
  // 自动构建索引和 RSS
  console.log('\n🔄 正在构建索引和 RSS...');
  import('./build-index.js').then(() => {
    import('./build-rss.js').then(() => {
      console.log('\n✅ 所有任务完成！');
    });
  });
}

generateWeekly();
