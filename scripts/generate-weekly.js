// 生成周刊 Markdown
import fs from 'fs';
import path from 'path';
import Handlebars from 'handlebars';

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
        summary: '组件通讯/生命周期/性能优化组件完整指南',
        description: '系统整理 Vue 组件通讯方案，配合性能优化组件实战。',
        source: '掘金',
        link: 'https://juejin.cn/frontend'
      }
    ],
    tools: [],
    projects: [],
    standards: [],
    articles: []
  };
  
  // 读取模板
  const templatePath = path.join(process.cwd(), 'scripts', 'template.hbs');
  const template = Handlebars.compile(fs.readFileSync(templatePath, 'utf-8'));
  const markdown = template(data);
  
  // 保存文件
  const archivesDir = path.join(process.cwd(), 'archives', weekInfo.year.toString());
  if (!fs.existsSync(archivesDir)) {
    fs.mkdirSync(archivesDir, { recursive: true });
  }
  
  const outputPath = path.join(archivesDir, `week-${weekInfo.weekNum}.md`);
  fs.writeFileSync(outputPath, markdown);
  
  console.log(`✅ 周刊已生成：${outputPath}`);
}

generateWeekly();
