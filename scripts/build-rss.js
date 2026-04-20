// 构建 RSS 订阅源
import fs from 'fs';
import path from 'path';
import { Feed } from 'feed';

function buildRSS() {
  const archivesDir = path.join(process.cwd(), 'archives');
  const indexFile = path.join(archivesDir, 'index.json');
  
  if (!fs.existsSync(indexFile)) {
    console.log('❌ 索引文件不存在，请先运行 npm run index');
    return;
  }
  
  const index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
  
  const feed = new Feed({
    title: '前端技术周刊',
    description: '每周一自动更新的前端技术周刊，帮你高效掌握前端趋势',
    id: 'https://github.com/WednesdayCAT/weekly-frontend-news',
    link: 'https://github.com/WednesdayCAT/weekly-frontend-news',
    language: 'zh-CN',
    favicon: 'https://github.githubassets.com/favicons/favicon.svg',
    copyright: 'MIT © WednesdayCAT',
    updated: new Date(index.updatedAt),
    generator: 'weekly-frontend-news',
    feedLinks: {
      rss: 'https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/rss.xml',
      json: 'https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/feed.json',
      atom: 'https://raw.githubusercontent.com/WednesdayCAT/weekly-frontend-news/main/atom.xml'
    },
    author: {
      name: 'WednesdayCAT',
      link: 'https://github.com/WednesdayCAT'
    }
  });
  
  // 添加最近 20 期周刊
  index.weeks.slice(0, 20).forEach(week => {
    const filePath = path.join(process.cwd(), 'archives', week.path);
    let content = '';
    
    if (fs.existsSync(filePath)) {
      content = fs.readFileSync(filePath, 'utf-8');
    }
    
    feed.addItem({
      title: week.title,
      id: week.url,
      link: week.url,
      description: `第${week.weekNum}周前端技术周刊`,
      content: content,
      author: [{ name: 'WednesdayCAT' }],
      date: new Date(week.updatedAt || Date.now())
    });
  });
  
  // 保存 RSS 文件
  fs.writeFileSync(path.join(process.cwd(), 'rss.xml'), feed.rss2());
  fs.writeFileSync(path.join(process.cwd(), 'feed.json'), feed.json1());
  fs.writeFileSync(path.join(process.cwd(), 'atom.xml'), feed.atom1());
  
  console.log(`✅ RSS 订阅源已生成（最近 ${Math.min(20, index.weeks.length)} 期）`);
}

buildRSS();
