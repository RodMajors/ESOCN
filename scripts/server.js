// 后端API服务器
import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';
import { load } from 'cheerio';
import fetch from 'node-fetch';

const app = express();
app.use(cors()); // 启用 CORS

// 创建数据库连接池 - eso_equipment
const equipmentPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_equipment',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// 创建数据库连接池 - esocp (用于cp_skills)
const cpSkillsPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esocp',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

// 现有的技能数据库配置（未使用连接池，保留以兼容现有代码）
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_skills',
};

// 无畏者誓约列表
const PledgeList1 = [
  "Spindleclutch II", "The Banished Cells I", "Fungal Grotto II", "Spindleclutch I",
  "Darkshade Caverns II", "Elden Hollow I", "Wayrest Sewers II", "Fungal Grotto I",
  "The Banished Cells II", "Darkshade Caverns I", "Elden Hollow II", "Wayrest Sewers I"
];

const PledgeList2 = [
  "Direfrost Keep", "Vaults of Madness", "Crypt of Hearts II", "City of Ash I",
  "Tempest Island", "Blackheart Haven", "Arx Corinium", "Selene's Web",
  "City of Ash II", "Crypt of Hearts I", "Volenfell", "Blessed Crucible"
];

const PledgeList3 = [
  "Imperial City Prison", "Ruins of Mazzatun", "White-Gold Tower", "Cradle of Shadows",
  "Bloodroot Forge", "Falkreath Hold", "Fang Lair", "Scalecaller Peak",
  "Moon Hunter Keep", "March of Sacrifices", "Depths of Malatar", "Frostvault",
  "Moongrave Fane", "Lair of Maarselok", "Icereach", "Unhallowed Grave",
  "Stone Garden", "Castle Thorn", "Black Drake Villa", "The Cauldron",
  "Red Petal Bastion", "The Dread Cellar", "Coral Aerie", "Shipwright's Regret",
  "Earthen Root Enclave", "Graven Deep", "Scrivener's Hall", "Bal Sunnar", "Oathsworn Pit", 
  "Bedlam Veil", 
];

// 计算无畏者更新
function getDailyPledges() {
  const startIndex1 = PledgeList1.indexOf("Darkshade Caverns II");
  const startIndex2 = PledgeList2.indexOf("Tempest Island");
  const startIndex3 = PledgeList3.indexOf("Bedlam Veil");

  const now = new Date();
  const startDate = new Date('2025-05-13T18:00:00');

  const timeDiff = now.getTime() - startDate.getTime();
  const hoursDiff = timeDiff / (1000 * 3600);
  const daysDiff = Math.floor(hoursDiff / 24);
  let rotationCount = daysDiff;
  if (now.getHours() < 18) {
    rotationCount--;
  }
  rotationCount = Math.max(0, rotationCount);

  const index1 = (startIndex1 + rotationCount) % PledgeList1.length;
  const index2 = (startIndex2 + rotationCount) % PledgeList2.length;
  const index3 = (startIndex3 + rotationCount) % PledgeList3.length;

  return {
    dailyPledges: [
      PledgeList1[index1],
      PledgeList2[index2],
      PledgeList3[index3]
    ],
    currentDate: now.toISOString()
  };
}

// 爬取服务器状态
async function scrapeServerStatus() {
  try {
    const statusList = {
      "PCEU": "", "PCNA": "", "PCPTS": "", "XBOXEU": "", "XBOXNA": "", "PSEU": "", "PSNA": ""
    };
    const url = 'https://esoserverstatus.net/';
    const res = await fetch(url);
    const statusData = await res.text();

    statusList.PCNA = statusData.split('PC-NA')[1].split('PC-PTS')[0].split('<b>')[1].split('</b>')[0];
    statusList.PCEU = statusData.split('PC-EU')[1].split('PC-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.PCPTS = statusData.split('PC-PTS')[1].split('XBOX-EU')[0].split('<b>')[1].split('</b>')[0];
    statusList.XBOXEU = statusData.split('XBOX-EU')[1].split('XBOX-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.XBOXNA = statusData.split('XBOX-NA')[1].split('PS4-EU')[0].split('<b>')[1].split('</b>')[0];
    statusList.PSEU = statusData.split('PS4-EU')[1].split('PS4-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.PSNA = statusData.split('PS4-NA')[1].split('/span')[0].split('<b>')[1].split('</b>')[0];

    return statusList;
  } catch (error) {
    console.error('爬取服务器状态失败:', error);
    return Array(7).fill('error');
  }
}

let cache = null;

// 计算下一次周一 18:00 CST
function getNextRefreshTime(now) {
  const date = new Date(now);
  const day = date.getDay(); // 0=周日，1=周一，...
  // 距离下周一的天数（如果今天是周一，+7天）
  const daysToNextMonday = day === 1 ? 7 : (8 - day) % 7;
  // 设置为下周一 18:00:00
  const nextMonday = new Date(date);
  nextMonday.setDate(date.getDate() + daysToNextMonday);
  nextMonday.setHours(18, 0, 0, 0);
  return nextMonday;
}

// 爬取函数
async function scrapeWeekTrialStatus() {
  const now = new Date();
  const defaultData = { PCNA: 'error', PCEU: 'error' };

  // 检查缓存
  if (cache && now >= cache.lastScraped && now < cache.nextRefresh) {
    console.log('使用缓存数据:', cache.data);
    return cache.data;
  }

  try {
    const url = 'https://eso-hub.com/';
    let res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } })
    if (!res.ok) throw new Error(`HTTP 错误: ${res.status}`);

    const weekData = await res.text();
    const trialsSection = weekData.split('Weekly Trials')[1];
    if (!trialsSection) throw new Error('未找到 Weekly Trials 部分');

    // 提取 PCNA 和 PCEU
    const pcnaMatch = trialsSection.split('PC NA')[1]?.split('span')[1]?.split('>')[1]?.split('</span>')[0]?.split('<')[0];
    const pceuMatch = trialsSection.split('PC EU')[1]?.split('span')[1]?.split('>')[1]?.split('</span>')[0]?.split('<')[0];

    if (!pcnaMatch || !pceuMatch) throw new Error('解析 PCNA 或 PCEU 失败');

    const data = {
      PCNA: pcnaMatch.trim(),
      PCEU: pceuMatch.trim(),
    };

    // 更新缓存
    cache = {
      data,
      lastScraped: now,
      nextRefresh: getNextRefreshTime(now),
    };
    console.log('爬取成功:', data, '下次刷新:', cache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取服务器状态失败:', error);
    return defaultData;
  }
}

// 一次性获取所有装备数据
app.get('/api/equipment/all', async (req, res) => {
  const query = `
    SELECT sets.*, 
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses,
           JSON_OBJECTAGG(styles.category, styles.sub_category) AS styles
    FROM sets
    LEFT JOIN bonuses ON sets.id = bonuses.set_id
    LEFT JOIN styles ON sets.id = styles.set_id
    GROUP BY sets.id
    ORDER BY sets.id DESC
  `;

  try {
    const [rows] = await equipmentPool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 分页查询套装列表
app.get('/api/equipment', async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const offset = (page - 1) * limit;

  const query = `
    SELECT * FROM sets
    ORDER BY id DESC
    LIMIT ? OFFSET ?
  `;
  const values = [parseInt(limit), parseInt(offset)];

  try {
    const [sets] = await equipmentPool.query(query, values);
    res.json(sets);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 根据地点查询相关套装
app.get('/api/equipment/related/:place', async (req, res) => {
  const { place } = req.params;
  const formattedPlace = decodeURIComponent(place).trim();
  const hexPlace = Buffer.from(formattedPlace, 'utf8').toString('hex').toUpperCase();

  const query = `
    SELECT sets.*, 
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses,
           (SELECT JSON_ARRAYAGG(styles.icon) 
            FROM styles 
            WHERE styles.set_id = sets.id) AS styles
    FROM sets
    LEFT JOIN bonuses ON sets.id = bonuses.set_id
    WHERE HEX(sets.place) = ?
    GROUP BY sets.id
    ORDER BY sets.id DESC
  `;

  try {
    const [rows] = await equipmentPool.query(query, [hexPlace]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 根据英文名查询套装详情
app.get('/api/equipment/:enName', async (req, res) => {
  const { enName } = req.params;
  const formattedEnName = decodeURIComponent(enName.replace(/_/g, '%20'));

  const query = `
    SELECT sets.*, 
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses,
           (SELECT JSON_ARRAYAGG(styles.icon) 
            FROM styles 
            WHERE styles.set_id = sets.id) AS styles
    FROM sets
    LEFT JOIN bonuses ON sets.id = bonuses.set_id
    WHERE sets.enName = ?
    GROUP BY sets.id
  `;

  try {
    const [rows] = await equipmentPool.query(query, [formattedEnName]);
    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到套装' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 获取所有技能数据（现有技能表）
app.get('/api/skills', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [classes] = await connection.execute('SELECT * FROM classes');
    const [skillTrees] = await connection.execute('SELECT * FROM skill_trees');
    const [skills] = await connection.execute('SELECT * FROM skills');
    const [skillVariants] = await connection.execute('SELECT * FROM skill_variants');
    await connection.end();

    res.json({
      classes,
      skill_trees: skillTrees,
      skills,
      skill_variants: skillVariants,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: '数据库查询失败' });
  }
});

// 新增：获取所有CP技能数据
app.get('/api/cp', async (req, res) => {
  const query = `
    SELECT *
    FROM cp_skills
    ORDER BY category_id, skill_index
  `;

  try {
    const [rows] = await cpSkillsPool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 新增：根据类别ID获取CP技能数据
app.get('/api/cp/:categoryId(\\d+)', async (req, res) => {
  const { categoryId } = req.params;

  const query = `
    SELECT *
    FROM cp_skills
    WHERE category_id = ?
    ORDER BY skill_index
  `;

  try {
    const parsedCategoryId = parseInt(categoryId);
    if (isNaN(parsedCategoryId)) {
      return res.status(400).json({ error: 'categoryId 必须是数字' });
    }
    const [rows] = await cpSkillsPool.query(query, [parsedCategoryId]);
    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到该类别的技能' });
    }
    res.json(rows);
  } catch (err) {
    console.error('Error in /api/cp/:categoryId:', { categoryId, error: err.message, stack: err.stack });
    res.status(500).json({ error: err.message });
  }
});

// 按en_name获取单个技能
app.get('/api/cp/:enName', async (req, res) => {
  const { enName } = req.params;
  if (!enName || typeof enName !== 'string') {
    console.warn('Invalid enName:', { enName });
    return res.status(400).json({ error: '无效的技能名称' });
  }

  const normalizedEnName = enName.replace(/_/g, ' ').trim();
  if (!normalizedEnName) {
    console.warn('Normalized enName is empty:', { enName, normalizedEnName });
    return res.status(400).json({ error: '技能名称不能为空' });
  }

  const query = `
    SELECT *
    FROM cp_skills
    WHERE en_name = ?
  `;

  try {
    const [rows] = await cpSkillsPool.query(query, [normalizedEnName]);
    if (rows.length === 0) {
      console.warn('Skill not found:', { enName, normalizedEnName });
      return res.status(404).json({ error: `未找到技能: ${enName}` });
    }
    res.json(rows[0]);
  } catch (err) {
    console.error('Error in /api/cp/:enName:', {
      enName,
      normalizedEnName,
      query,
      error: err.message,
      stack: err.stack
    });
    res.status(500).json({ error: err.message });
  }
});

// 获取每日无畏者誓约
app.get('/api/daily-pledges', (req, res) => {
  const result = getDailyPledges();
  res.json(result);
});

// 获取服务器状态
app.get('/api/server-status', async (req, res) => {
  const statusList = await scrapeServerStatus();
  res.json({
    status: statusList,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/week-trial', async (req, res) => {
  const statusList = await scrapeWeekTrialStatus();
  res.json({
    status: statusList,
    timestamp: new Date().toISOString()
  });
});

// 启动服务器
app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});