// 周刊元数据管理
import fs from 'fs';
import path from 'path';

const METADATA_FILE = path.join(process.cwd(), 'archives', 'metadata.json');

export function loadMetadata() {
  if (fs.existsSync(METADATA_FILE)) {
    return JSON.parse(fs.readFileSync(METADATA_FILE, 'utf-8'));
  }
  return { weeks: [] };
}

export function saveMetadata(metadata) {
  fs.writeFileSync(METADATA_FILE, JSON.stringify(metadata, null, 2));
}

export function addWeekMetadata(weekData) {
  const metadata = loadMetadata();
  
  // 检查是否已存在
  const exists = metadata.weeks.some(
    w => w.year === weekData.year && w.weekNum === weekData.weekNum
  );
  
  if (exists) {
    console.log(`⚠️  ${weekData.year}年第${weekData.weekNum}周已存在`);
    return false;
  }
  
  metadata.weeks.push({
    year: weekData.year,
    weekNum: weekData.weekNum,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    stats: {
      frameworkUpdates: weekData.frameworkUpdates || 0,
      tools: weekData.tools || 0,
      projects: weekData.projects || 0,
      standards: weekData.standards || 0,
      articles: weekData.articles || 0
    }
  });
  
  saveMetadata(metadata);
  console.log(`✅ 元数据已更新：${weekData.year}年第${weekData.weekNum}周`);
  return true;
}

export function getWeekStats() {
  const metadata = loadMetadata();
  
  const totalStats = {
    totalWeeks: metadata.weeks.length,
    totalItems: 0,
    avgItemsPerWeek: 0
  };
  
  metadata.weeks.forEach(week => {
    totalStats.totalItems += Object.values(week.stats).reduce((a, b) => a + b, 0);
  });
  
  totalStats.avgItemsPerWeek = totalStats.totalWeeks > 0 
    ? Math.round(totalStats.totalItems / totalStats.totalWeeks) 
    : 0;
  
  return totalStats;
}

// CLI 模式
if (process.argv[1].includes('metadata.js')) {
  const action = process.argv[2];
  
  if (action === 'stats') {
    const stats = getWeekStats();
    console.log('📊 周刊统计:');
    console.log(`   总期数：${stats.totalWeeks}`);
    console.log(`   总条目：${stats.totalItems}`);
    console.log(`   平均每周期：${stats.avgItemsPerWeek} 条`);
  } else {
    console.log('用法：node scripts/metadata.js stats');
  }
}
