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
  connectionLimit: 1000 ,
  queueLimit: 0,
});

// 创建数据库连接池 - esocp (用于cp_skills)
const cpSkillsPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esocp2',
  waitForConnections: true,
  connectionLimit: 1000 ,
  queueLimit: 0,
});

// 创建数据库连接池 - esocp (用于cp_skills)
const foodPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_foods',
  waitForConnections: true,
  connectionLimit: 1000 ,
  queueLimit: 0,
});

const furniturePool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_furniture',
  waitForConnections: true,
  connectionLimit: 1000 ,
  queueLimit: 0,
});

const newsPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esonews',
  waitForConnections: true,
  connectionLimit: 1000 ,
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
  "Bedlam Veil", "Lep Seclusa", "Exiled Redoubt"
];

// 计算无畏者更新
function getDailyPledges() {
  const startIndex1 = PledgeList1.indexOf("Fungal Grotto II");
  const startIndex2 = PledgeList2.indexOf("Crypt of Hearts II");
  const startIndex3 = PledgeList3.indexOf("Scalecaller Peak");

  const now = new Date();
  const startDate = new Date('2025-05-22T18:00:00');

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

let WeekTrialCache = null;
let patchNotesCache = null;
let goldenVendorCache = null; // 新增缓存变量

// 计算下一次周一 18:00 CST
function getNextRefreshTime(now) {
  const date = new Date(now);
  const day = date.getDay(); // 0=周日，1=周一，...
  const daysToNextMonday = day === 1 ? 7 : (8 - day) % 7;
  const nextMonday = new Date(date);
  nextMonday.setDate(date.getDate() + daysToNextMonday);
  nextMonday.setHours(18, 0, 0, 0);
  return nextMonday;
}

// 计算下一次周六 08:00 CST
function getNextSaturdayRefreshTime(now) {
  const date = new Date(now);
  const day = date.getDay(); // 0=周日，1=周一，...，6=周六
  const daysToNextSaturday = day === 6 ? 7 : (6 - day + 7) % 7;
  const nextSaturday = new Date(date);
  nextSaturday.setDate(date.getDate() + daysToNextSaturday);
  nextSaturday.setHours(8, 0, 0, 0);
  return nextSaturday;
}

// 爬取周试炼状态
async function scrapeWeekTrialStatus() {
  const now = new Date();
  const defaultData = { PCNA: 'error', PCEU: 'error' };

  if (WeekTrialCache && now >= WeekTrialCache.lastScraped && now < WeekTrialCache.nextRefresh) {
    console.log('使用缓存数据:', WeekTrialCache.data);
    return WeekTrialCache.data;
  }

  try {
    const url = 'https://eso-hub.com/';
    let res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) throw new Error(`HTTP 错误: ${res.status}`);

    const weekData = await res.text();
    const trialsSection = weekData.split('Weekly Trials')[1];
    if (!trialsSection) throw new Error('未找到 Weekly Trials 部分');

    const pcnaMatch = trialsSection.split('PC NA')[1]?.split('span')[1]?.split('>')[1]?.split('</span>')[0]?.split('<')[0];
    const pceuMatch = trialsSection.split('PC EU')[1]?.split('span')[1]?.split('>')[1]?.split('</span>')[0]?.split('<')[0];

    if (!pcnaMatch || !pceuMatch) throw new Error('解析 PCNA 或 PCEU 失败');

    const data = {
      PCNA: pcnaMatch.trim().replace(/&#039;/g, "'"),
      PCEU: pceuMatch.trim().replace(/&#039;/g, "'"),
    };

    WeekTrialCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextRefreshTime(now),
    };
    console.log('爬取成功:', data, '下次刷新:', WeekTrialCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取服务器状态失败:', error);
    return defaultData;
  }
}

// 爬取补丁笔记数据
async function scrapePatchNotes() {
  const now = new Date();
  const defaultData = { PC: { href: 'error', img: 'error' }, XBOX: { href: 'error', img: 'error' }, PS: { href: 'error', img: 'error' }, PTS: { href: 'error', img: 'error' } };

  if (patchNotesCache && now >= patchNotesCache.lastScraped && now < patchNotesCache.nextRefresh) {
    console.log('使用缓存数据:', patchNotesCache.data);
    return patchNotesCache.data;
  }

  try {
    const patchNotesUrl = 'https://forums.elderscrollsonline.com/en/categories/patch-notes';
    const patchNotesRes = await fetch(patchNotesUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const patchNotesHtml = await patchNotesRes.text();
    const $patchNotes = load(patchNotesHtml);

    const trs = $patchNotes('table tbody tr');
    const psHref = trs.eq(0).find('.DiscussionName .Wrap a').attr('href');
    const xboxHref = trs.eq(1).find('.DiscussionName .Wrap a').attr('href');
    const pcHref = trs.eq(2).find('.DiscussionName .Wrap a').attr('href');

    const ptsUrl = 'https://forums.elderscrollsonline.com/en/categories/pts';
    const ptsRes = await fetch(ptsUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const ptsHtml = await ptsRes.text();
    const $pts = load(ptsHtml);
    const ptsHref = $pts('table tbody tr').eq(0).find('.DiscussionName .Wrap a').attr('href');

    async function getImg(href) {
      if (!href) return 'error';
      const res = await fetch(href, { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const html = await res.text();
      const $ = load(html);
      return $('img').eq(1).attr('src') || 'error';
    }

    const [psImg, xboxImg, pcImg, ptsImg] = await Promise.all([
      getImg(psHref),
      getImg(xboxHref),
      getImg(pcHref),
      getImg(ptsHref)
    ]);

    const data = {
      PS: { href: psHref || 'error', img: psImg },
      XBOX: { href: xboxHref || 'error', img: xboxImg },
      PC: { href: pcHref || 'error', img: pcImg },
      PTS: { href: ptsHref || 'error', img: ptsImg }
    };

    patchNotesCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextRefreshTime(now),
    };
    console.log('爬取成功:', data, '下次刷新:', patchNotesCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取补丁笔记失败:', error);
    return defaultData;
  }
}

// 新增：爬取金色商人数据
async function scrapeGoldenVendor() {
  const now = new Date();
  const defaultData = { items: [], time: 'error' };

  if (goldenVendorCache && now >= goldenVendorCache.lastScraped && now < goldenVendorCache.nextRefresh) {
    console.log('使用缓存数据:', goldenVendorCache.data);
    return goldenVendorCache.data;
  }

  try {
    const url = 'https://esoitem.uesp.net/goldenVendor.php';
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) throw new Error(`HTTP 错误: ${res.status}`);
    const html = await res.text();
    const $ = load(html);

    // 提取时间
    let time = 'error';
    const h4Text = $('h4').first().text().trim();
    const dateMatch = h4Text.replace('Vendor Items for ', '');
    if (dateMatch) {
      const startDate = new Date(dateMatch);
      if (!isNaN(startDate)) {
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 1);
        const formatDate = (date) => `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
        time = `${formatDate(startDate)}-${formatDate(endDate)}`;
      }
    }

    // 英中特质对照表
    const traitMap = {
      "Divines": "神性",
      "Nirnhoned": "奈恩磨砺",
      "Sturdy": "强韧",
      "Impenetrable": "牢不可破",
      "Reinforced": "强化防御",
      "Well-Fitted": "合身",
      "Training": "训练",
      "Infused": "注魔",
      "Invigorating": "活力再生",
      "Precise": "精准",
      "Sharpened": "锋锐",
      "Charged": "充能",
      "Defending": "防御",
      "Decisive": "决意",
      "Powered": "动力",
      "Harmony": "和谐",
      "Bloodthirsty": "嗜血",
      "Arcane": "奥术",
      "Healthy": "健康",
      "Robust": "强壮",
      "Protective": "保护",
      "Swift": "轻灵",
      "Triune": "三体"
    };

    const items = [];
    const listItems = $('h4').first().next('ul.uespesoGoldenItemList').find('li');

    for (let i = 0; i < listItems.length; i++) {
      const li = listItems.eq(i);
      const raw = li.find('span.uespesoGoldenItem').text().trim();
      const href = li.find('a.uespesoItemLink').attr('href');

      // 提取 gp 和 ap
      const priceText = li.text().split('--')[1]?.trim();
      const gpMatch = priceText?.match(/(\d+)\s*gp/)?.[1];
      const apMatch = priceText?.match(/(\d+)\s*AP/)?.[1];

      // 解析 traits
      let traits = [];
      const match = raw.match(/^(.*?)\s*\((.*?)\)$/);
      if (match) {
        traits = match[2].split('/').map(t => t.trim()).filter(t => t);
        traits = traits.map(t => traitMap[t] || t); // 转换为中文，未匹配的特质保持原样
      }

      // 获取 setName 和 icon
      let setName = 'error';
      let icon = 'error';
      if (href) {
        const itemRes = await fetch(href, { headers: { 'User-Agent': 'Mozilla/5.0' } });
        const itemHtml = await itemRes.text();
        const $item = load(itemHtml);
        setName = $item('td#esoil_rawdata_setName').text().trim() || 'error';
        const iconText = $item('td#esoil_rawdata_icon').text().trim();
        const iconMatch = iconText.match(/(\/esoui\/art\/icons\/[^ ]+\.dds)/);
        icon = iconMatch ? iconMatch[1].replace('.dds', '.webp') : 'error';
      }

      items.push({
        setName,
        traits,
        gp: gpMatch || 'error',
        ap: apMatch || 'error',
        icon
      });
    }

    const data = { items, time };
    goldenVendorCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextSaturdayRefreshTime(now),
    };
    console.log('爬取金色商人成功:', data, '下次刷新:', goldenVendorCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取金色商人失败:', error);
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

// 获取所有CP技能数据
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

// 根据类别ID获取CP技能数据
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

// 获取周试炼状态
app.get('/api/week-trial', async (req, res) => {
  const statusList = await scrapeWeekTrialStatus();
  res.json({
    status: statusList,
    timestamp: new Date().toISOString()
  });
});

// 获取补丁笔记数据
app.get('/api/patch-notes', async (req, res) => {
  const data = await scrapePatchNotes();
  res.json({
    data,
    timestamp: new Date().toISOString()
  });
});

// 新增：获取金色商人数据
app.get('/api/golden-vendor', async (req, res) => {
  const data = await scrapeGoldenVendor();
  res.json({
    data: data.items,
    time: data.time,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/foods', async (req, res) => {
  const query = `
    SELECT *
    FROM foods
    ORDER BY id DESC
  `;

  try {
    const [rows] = await foodPool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/foods/:enName', async (req, res) => {
  const { enName } = req.params;
  const formattedEnName = decodeURIComponent(enName.replace(/_/g, '%20'));

  const query = `
    SELECT *
    FROM foods
    WHERE enName = ?
  `;

  try {
    const [rows] = await foodPool.query(query, [formattedEnName]);
    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到食物' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
})

app.get('/api/furniture', async (req, res) => {
  const query = `
    SELECT *
    FROM furniture
    ORDER BY id DESC
  `;

  try {
    const [rows] = await furniturePool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/furniture/:enName', async (req, res) => {
  const { enName } = req.params;
  const formattedEnName = decodeURIComponent(enName.replace(/_/g, '%20'));

  const query = `
    SELECT *
    FROM furniture
    WHERE enName = ?
  `;

  try {
    const [rows] = await furniturePool.query(query, [formattedEnName]);
    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到家具' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/news', async (req, res) => {
  const query = `
    SELECT *
    FROM newsList
    ORDER BY id DESC
  `;

  try {
    const [rows] = await newsPool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/news/:id(\\d+)', async (req, res) => {
  const { id } = req.params;

  const query = `
    SELECT *
    FROM newsList
    WHERE id = ?
  `;

  try {
    const [rows] = await newsPool.query(query, [parseInt(id)]);
    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到新闻' });
    }
    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 启动服务器
app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});