// 构建周刊索引
import fs from 'fs';
import path from 'path';

function buildIndex() {
  const archivesDir = path.join(process.cwd(), 'archives');
  const indexFile = path.join(archivesDir, 'index.json');
  
  const index = {
    updatedAt: new Date().toISOString(),
    totalWeeks: 0,
    weeks: []
  };
  
  // 遍历所有年份目录
  if (fs.existsSync(archivesDir)) {
    const years = fs.readdirSync(archivesDir)
      .filter(dir => /^\d{4}$/.test(dir));
    
    years.forEach(year => {
      const yearDir = path.join(archivesDir, year);
      const files = fs.readdirSync(yearDir)
        .filter(f => f.endsWith('.md'))
        .sort();
      
      files.forEach(file => {
        const weekNum = file.match(/week-(\d+)\.md/);
        if (weekNum) {
          const filePath = path.posix.join(year, file);
          const content = fs.readFileSync(path.join(yearDir, file), 'utf-8');
          
          // 提取标题
          const titleMatch = content.match(/# 📅 (\d{4}-\d+ 周)/);
          const dateMatch = content.match(/更新时间：(\d{4}-\d{2}-\d{2})/);
          
          index.weeks.push({
            year: parseInt(year),
            weekNum: parseInt(weekNum[1]),
            title: titleMatch ? titleMatch[1] : `${year}年第${weekNum[1]}周`,
            updatedAt: dateMatch ? dateMatch[1] : null,
            path: filePath,
            url: `https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/${filePath}`
          });
        }
      });
    });
  }
  
  // 按年份和周数排序
  index.weeks.sort((a, b) => {
    if (a.year !== b.year) return b.year - a.year;
    return b.weekNum - a.weekNum;
  });
  
  index.totalWeeks = index.weeks.length;
  
  // 写入索引文件
  fs.writeFileSync(indexFile, JSON.stringify(index, null, 2));
  console.log(`✅ 索引已构建：共 ${index.totalWeeks} 期周刊`);
  
  // 同时生成 Markdown 索引
  generateMarkdownIndex(index);
}

function generateMarkdownIndex(index) {
  let md = `# 📚 周刊存档索引\n\n`;
  md += `> 共 ${index.totalWeeks} 期周刊 | 最后更新：${index.updatedAt.split('T')[0]}\n\n`;
  md += `---\n\n`;
  
  // 按年份分组
  const byYear = {};
  index.weeks.forEach(week => {
    if (!byYear[week.year]) byYear[week.year] = [];
    byYear[week.year].push(week);
  });
  
  Object.keys(byYear).sort((a, b) => b - a).forEach(year => {
    md += `## ${year}年\n\n`;
    md += `| 期数 | 标题 | 更新日期 | 链接 |\n`;
    md += `|------|------|----------|------|\n`;
    
    byYear[year].forEach(week => {
      md += `| ${week.weekNum} | ${week.title} | ${week.updatedAt || '-'} | [查看](${week.path}) |\n`;
    });
    
    md += `\n`;
  });
  
  const mdIndexFile = path.join(process.cwd(), 'archives', 'README.md');
  fs.writeFileSync(mdIndexFile, md);
  console.log(`✅ Markdown 索引已生成`);
}

buildIndex();
