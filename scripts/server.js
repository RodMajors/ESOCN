// 后端API服务器
import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';
import { load } from 'cheerio';
import fetch from 'node-fetch';
import { promises as fs } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';
import puppeteer from 'puppeteer';

// 将 exec 转为返回 Promise 的函数
const execPromise = promisify(exec);
const app = express();
app.use(cors()); // 启用 CORS

let WeekTrialCache = null;
let patchNotesCache = null;
let goldenVendorCache = null;
let LuxuryFurnisherCache = null;
let InfiniteVendorCache = null; 
let TelVarVendorCache = null;
let DailyLoginRewardsCache = null;

// 创建数据库连接池 - eso_equipment
const equipmentPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_equipment',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

// 创建数据库连接池 - esocp (用于cp_skills)
const cpSkillsPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esocp',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

// 创建数据库连接池 - eso_foods
const foodPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_foods',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

// 创建数据库连接池 - eso_furniture
const furniturePool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_furniture',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

// 创建数据库连接池 - esonews
const newsPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esonews',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

// 现有的技能数据库配置（未使用连接池，保留以兼容现有代码）
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_skills',
};

const dataPool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'esodata',
  waitForConnections: true,
  connectionLimit: 1000,
  queueLimit: 0,
});

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

function getLastMonthRefreshTime(now) {
  const date = new Date(now);
  date.setUTCDate(1);
  date.setUTCHours(12, 0, 0, 0);
  date.setUTCMonth(date.getUTCMonth() + 1);
  return date;
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

// 计算下一次周三 08:00 CST（北京时间）
function getNextWednesdayRefreshTime(now) {
  const date = new Date(now);
  const day = date.getDay(); // 0=周日，1=周一，...，3=周三
  const daysToNextWednesday = day === 3 ? 7 : (3 - day + 7) % 7;
  const nextWednesday = new Date(date);
  nextWednesday.setDate(date.getDate() + daysToNextWednesday);
  nextWednesday.setHours(8, 0, 0, 0); // 北京时间 08:00
  return nextWednesday;
}

// 计算上一次周三 08:00 CST（北京时间）
function getLastWednesdayRefreshTime(now) {
  const date = new Date(now);
  const day = date.getDay(); // 0=周日，1=周一，...，3=周三
  const daysSinceLastWednesday = day >= 3 ? day - 3 : day + 4;
  const lastWednesday = new Date(date);
  lastWednesday.setDate(date.getDate() - daysSinceLastWednesday);
  lastWednesday.setHours(8, 0, 0, 0); // 北京时间 08:00
  return lastWednesday;
}

async function getNews() {
  try {
    // 读取 last-time.txt 文件
    const data = await fs.readFile('./src/Data/last-time.txt', 'utf8');
    const timestampInSeconds = parseInt(data.trim(), 10);

    if (isNaN(timestampInSeconds)) {
      console.error('无效的时间戳在 last-time.txt 中');
      return;
    }

    // 将秒级时间戳转换为毫秒
    const timestamp = timestampInSeconds * 1000;

    // 获取当前北京时间
    const now = new Date();
    const beijingOffset = 8 * 60 * 60 * 1000; // 北京时间 UTC+8
    const beijingNow = new Date(now.getTime() + beijingOffset);

    // 获取北京时间今天的 0 点
    const todayMidnight = new Date(Date.UTC(
      beijingNow.getUTCFullYear(),
      beijingNow.getUTCMonth(),
      beijingNow.getUTCDate()
    ) - beijingOffset);

    // 调试：输出时间戳
    console.log(`last-time.txt timestamp: ${timestamp} (${new Date(timestamp).toUTCString()})`);
    console.log(`todayMidnight: ${todayMidnight.getTime()} (${todayMidnight.toUTCString()})`);

    // 判断时间戳是否为“昨天”（早于今天 0 点）
    if (timestamp < todayMidnight.getTime()) {
      console.log('最新新闻是昨天的，执行 news.py');
      // 执行 news.py 并等待完成
      try {
        const { stdout, stderr } = await execPromise('python ./scripts/news.py');
        if (stderr) {
          console.error(`Error executing news.py: ${stderr}`);
        } else {
          console.log(`news.py executed successfully: ${stdout}`);
        }
      } catch (error) {
        console.error(`Failed to execute news.py: ${error.message}`);
      }
    } else {
      console.log('最新新闻是今天的，不需要执行 news.py');
    }
  } catch (error) {
    console.error(`Error reading last-time.txt: ${error.message}`);
  }
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
      PCNA: pcnaMatch.trim().replace(/&#039;/g, "'").replace(/’/g, "'"),
      PCEU: pceuMatch.trim().replace(/&#039;/g, "'").replace(/’/g, "'"),
    };

    WeekTrialCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextRefreshTime(now),
    };

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
    const psHref = trs.eq(2).find('.DiscussionName .Wrap a').attr('href');
    const xboxHref = trs.eq(3).find('.DiscussionName .Wrap a').attr('href');
    const pcHref = trs.eq(1).find('.DiscussionName .Wrap a').attr('href');

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

async function scrapeLuxuryFurnisher() {
  const now = new Date();
  const defaultData = { items: [], timestamp: 'error' };

  if (LuxuryFurnisherCache && now >= LuxuryFurnisherCache.lastScraped && now < LuxuryFurnisherCache.nextRefresh) {
    console.log('使用豪华家具商缓存数据:', LuxuryFurnisherCache.data);
    return LuxuryFurnisherCache.data;
  }

  try {
    const url = 'https://en.uesp.net/wiki/Online:Furnishings/Luxury_Furnisher';
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) throw new Error(`HTTP 错误: ${res.status}`);
    const html = await res.text();
    const $ = load(html);

    const items = [];
    const rows = $('table.wikitable.sortable tbody tr');
    rows.each((i, row) => {
      const tds = $(row).find('td');
      // 确保行有足够的列（至少 6 列：Image, Name, Type, Cost, Date, Description）
      if (tds.length < 6) {
        console.warn(`第 ${i + 1} 行列数不足，跳过: ${$(row).text().trim().slice(0, 50)}...`);
        return;
      }

      const nameCell = tds.eq(1); // 第二列（Name）
      const costCell = tds.eq(3); // 第四列（Cost）
      const nameLink = nameCell.find('a.eso_item_link').text().trim();
      
      // 获取 data-sort-value
      let costText = costCell.attr('data-sort-value');
      // 如果 data-sort-value 缺失，尝试从文本提取
      if (!costText) {
        costText = costCell.find('span').eq(1).text().trim().replace(/[^\d,]/g, '');
        console.warn(`第 ${i + 1} 行缺少 data-sort-value，使用文本内容: ${costText}`);
      }

      // 确保 costText 有效
      if (!costText) {
        console.warn(`第 ${i + 1} 行 Cost 数据无效，跳过: name=${nameLink}`);
        return;
      }

      const cost = parseInt(costText.replace(/,/g, ''), 10);

      if (nameLink && !isNaN(cost)) {
        items.push({ name: nameLink, cost });
      } else {
        console.warn(`第 ${i + 1} 行数据无效，跳过: name=${nameLink}, cost=${cost}`);
      }
    });

    if (items.length === 0) throw new Error('未找到豪华家具商物品');

    const data = { items, timestamp: now.toISOString() };
    LuxuryFurnisherCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextSaturdayRefreshTime(now),
    };
    console.log('爬取豪华家具商成功:', data, '下次刷新:', LuxuryFurnisherCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取豪华家具商失败:', error);
    return defaultData;
  }
}

// 新增：爬取 Filer Ool 数据
// 新增：爬取 Infinite Vendor (Filer Ool) 数据
async function scrapeInfiniteVendor() {
  const now = new Date();
  const defaultData = { items: [], time: 'error' };

  if (InfiniteVendorCache && now >= InfiniteVendorCache.lastScraped && now < InfiniteVendorCache.nextRefresh) {
    console.log('使用 Infinite Vendor 缓存数据:', InfiniteVendorCache.data);
    return InfiniteVendorCache.data;
  }

  try {
    const url = 'https://en.uesp.net/wiki/Online:Filer_Ool';
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) throw new Error(`HTTP 错误: ${res.status}`);
    const html = await res.text();
    const $ = load(html);

    // 选择正确的表格：class 包含 wikitable 和 sortable
    const tables = $('table.wikitable.sortable');
    if (tables.length === 0) throw new Error('未找到 wikitable.sortable 表格');
    console.log(`找到 ${tables.length} 个 wikitable.sortable 表格`);

    const items = [];
    const rows = tables.first().find('tbody tr');
    if (rows.length === 0) throw new Error('表格中未找到行');

    // 收集所有行的数据，稍后批量查询 zhText
    const rowData = [];
    rows.each((i, row) => {
      const tds = $(row).find('td');
      if (tds.length < 5) {
        console.warn(`第 ${i + 1} 行列数不足，跳过: ${$(row).text().trim().slice(0, 50)}...`);
        return;
      }

      const iconCell = tds.eq(0); // 第一列（Icon）
      const nameCell = tds.eq(1); // 第二列（Name）
      const valueCell = tds.eq(2); // 第三列（Value）

      // 提取 icon
      const icon = "https:" + (iconCell.find('img').attr('src')?.replace(/\/thumb\//, '/').replace(/\/48px-.*/, '') || 'error');

      // 提取 enName
      const enName = nameCell.find('a.eso_item_link').text().trim() || 'error';

      // 提取 value
      let value;
      const displayValue = valueCell.find('span.esoqclegendary.coloredlinks').text().trim();
      if (displayValue) {
        value = displayValue.replace(/[^\d]/g, ''); // 移除逗号、空格等非数字字符
      } else {
        const sortValue = valueCell.attr('data-sort-value');
        if (sortValue) {
          value = parseInt(sortValue, 10).toString(); // 去除前导零
        } else {
          value = valueCell.text().trim().replace(/[^\d]/g, '') || 'error';
        }
      }

      // 提取颜色（根据 quality 属性映射）
      const qualityClass = nameCell.find('a.eso_item_link').attr('class') || '';
      let color = '#FFFFFF'; // 默认白色
      if (qualityClass.includes('eso_item_link_q3')) {
        color = '#3A92FF'; // 蓝色
      } else if (qualityClass.includes('eso_item_link_q4')) {
        color = '#A800A8'; // 紫色
      } else if (qualityClass.includes('eso_item_link_q5')) {
        color = '#EE8310'; // 金色
      }

      if (enName !== 'error' && value !== 'error') {
        rowData.push({ icon, enName, value, color });
      } else {
        console.warn(`第 ${i + 1} 行数据无效，跳过: enName=${enName}, value=${value}, displayValue=${displayValue}, dataSortValue=${valueCell.attr('data-sort-value')}, rawValue=${valueCell.text().trim()}`);
      }
    });

    // 批量查询 zhText
    for (const row of rowData) {
      let trueEnName ;
      let flag = false ;
      if(row.enName === "Lead: Auri-El Metal Carvings")
        flag = true;

      if (row.enName.startsWith('Lead: ')) {
        trueEnName = row.enName.replace('Lead: ', '');
        flag = true;
      } else {
        trueEnName = row.enName;
      }
      try {
        const query = `
          SELECT zhText
          FROM esoText
          WHERE enText = ?
          ORDER BY id DESC
          LIMIT 1
        `;
        const [results] = await dataPool.query(query, [trueEnName]);
        let zhName = results.length > 0 ? results[0].zhText : trueEnName; // 回退到 enName
        if (flag) 
          zhName = '线索：'+ zhName; // 如果是 Lead，添加前缀
        items.push({ icon: row.icon, name: zhName, enName: row.enName, value: row.value, color: row.color });
      } catch (dbError) {
        console.warn(`查询 zhText 失败，enName=${trueEnName}，使用英文名: ${dbError.message}`);
        items.push({ icon: row.icon, name: row.enName, enName: row.enName, value: row.value, color: row.color });
      }
    }

    if (items.length === 0) throw new Error('未找到 Infinite Vendor 物品');

    // 计算时间范围
    const lastWednesday = getLastWednesdayRefreshTime(now);
    const nextWednesday = getNextWednesdayRefreshTime(now);
    const formatDate = (date) => `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    const time = `${formatDate(lastWednesday)}-${formatDate(nextWednesday)}`;

    const data = { items, time };
    InfiniteVendorCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextWednesdayRefreshTime(now),
    };
    console.log('爬取 Infinite Vendor 成功:', data, '下次刷新:', InfiniteVendorCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取 Infinite Vendor 失败:', error);
    return defaultData;
  }
}

async function scrapeTelVarVendor() {
  const now = new Date();
  const defaultData = { items: [], time: 'error' };

  if (TelVarVendorCache && now.getTime() >= TelVarVendorCache.lastScraped.getTime() && now.getTime() < TelVarVendorCache.nextRefresh.getTime()) {
    console.log('使用 Tel Var Vendor 缓存数据:', TelVarVendorCache.data);
    return TelVarVendorCache.data;
  }

  let browser;
  try {
    const url = 'https://eso-hub.com/en/weekly-ic-tel-var-merchant';
    let attempts = 0;
    const maxAttempts = 3;
    let html;

    while (attempts < maxAttempts) {
      attempts++;
      try {
        // 启动 Puppeteer
        browser = await puppeteer.launch({
          headless: true,
          args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security'],
          executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        });
        const page = await browser.newPage();

        // 设置 User-Agent 和视口
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36');
        await page.setViewport({ width: 1280, height: 800 });

        // 增加伪装
        await page.setExtraHTTPHeaders({
          'Accept-Language': 'en-US,en;q=0.9',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        });

        // 访问页面
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
        await page.waitForSelector('body', { timeout: 30000 });

        // 检查 Cloudflare
        const title = await page.title();
        if (title.includes('Just a moment') || title.includes('Access denied')) {
          throw new Error(`Cloudflare 拦截，标题: ${title}`);
        }

        // 等待网格加载
        await page.waitForSelector('div.grid', { timeout: 30000 });

        // 获取页面 HTML
        html = await page.content();
        break;
      } catch (error) {
        console.warn(`尝试 ${attempts} 失败: ${error.message}`);
        if (attempts === maxAttempts) throw error;
        if (browser) await browser.close().catch(() => {});
        await new Promise(resolve => setTimeout(resolve, 2000 * attempts));
      }
    }

    const $ = load(html);

    // 选择第一个目标网格
    const grid = $('div.grid[class*="grid-cols-[repeat(auto-fill,minmax(350px,1fr))]"]').eq(0);
    if (!grid.length) {
      console.warn('HTML 内容:', html.slice(0, 500));
      console.warn('所有网格类:', $('div.grid').map((i, el) => $(el).attr('class')).get());
      throw new Error('未找到目标网格');
    }
    console.log(`找到第一个目标网格，类: ${grid.attr('class')}`);

    const items = [];
    // 选择网格的直接子节点
    const itemDivs = grid.children('div').filter((i, el) => {
      const $el = $(el);
      return $el.find('img').length && $el.find('a.text-lg.text-pretty').length && $el.find('div.text-white\\/75').text().includes('Tel var stones');
    });
    if (itemDivs.length === 0) {
      console.warn('未找到物品，网格 HTML:', grid.html().slice(0, 500));
      throw new Error('未找到物品');
    }
    console.log(`找到 ${itemDivs.length} 个物品`);

    // 收集所有物品数据
    const rowData = [];
    itemDivs.each((i, div) => {
      const $div = $(div);

      // 提取 icon
      const iconSrc = $div.find('img').attr('src') || 'error';
      const icon = iconSrc.startsWith('http') ? iconSrc : 'https://eso-hub.com' + iconSrc;

      // 提取 enName
      const nameLink = $div.find('a.text-lg.text-pretty');
      const enName = nameLink.text().trim() || 'error';

      // 提取 color
      const colorStyle = nameLink.attr('style') || '';
      const color = colorStyle.match(/color:\s*(rgb\([^)]+\)|#[0-9a-fA-F]+)/i)?.[1] || '#FFFFFF';

      // 提取 value
      const valueText = $div.find('div.text-white\\/75').text().trim();
      const valueMatch = valueText.match(/([\d,]+)\s*Tel var stones/i);
      const value = valueMatch ? valueMatch[1].replace(/,/g, '') : 'error';

      if (enName !== 'error' && value !== 'error' && icon !== 'error') {
        rowData.push({ icon, enName, color, value });
      } else {
        console.warn(`第 ${i + 1} 项数据无效，跳过: enName=${enName}, value=${value}, icon=${icon}, valueText=${valueText}`);
      }
    });

    // 批量查询 zhText
    for (const row of rowData) {
      let flag = false;
      let trueEnName = row.enName;
      if (row.enName.startsWith('Lead: ')){
        trueEnName = row.enName.replace('Lead: ', '');
        flag = true;
      }
      try {
        const query = `
          SELECT zhText
          FROM esoText
          WHERE enText = ?
          ORDER BY id DESC
          LIMIT 1
        `;
        const [results] = await dataPool.query(query, [trueEnName]);
        let zhName = results.length > 0 ? results[0].zhText : row.enName;
        if (flag)
          zhName = '线索：' + zhName; // 如果是 Lead，添加前缀
        items.push({ icon: row.icon, name: zhName, enName: row.enName, color: row.color, value: row.value });
      } catch (dbError) {
        console.warn(`查询 zhText 失败，enName=${row.enName}，使用英文名: ${dbError.message}`);
        items.push({ icon: row.icon, name: row.enName,  enName: row.enName, color: row.color,value: row.value });
      }
    }

    if (items.length === 0) {
      console.warn('物品数量为 0，网格 HTML:', grid.html().slice(0, 500));
      throw new Error('未找到 Tel Var Vendor 物品');
    }

    // 计算时间范围
    const lastWednesday = getLastWednesdayRefreshTime(now);
    const nextWednesday = getNextWednesdayRefreshTime(now);
    const formatDate = (date) => `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
    const time = `${formatDate(lastWednesday)}-${formatDate(nextWednesday)}`;

    const data = { items, time };
    TelVarVendorCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextWednesdayRefreshTime(now),
    };
    console.log('爬取 Tel Var Vendor 成功:', data, '下次刷新:', TelVarVendorCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取 Tel Var Vendor 失败:', error);
    return defaultData;
  } finally {
    if (browser) await browser.close().catch(err => console.warn('关闭浏览器失败:', err));
  }
}

async function scrapeDailyLoginRewards() {
  const now = new Date();
  const defaultData = { items: [], time: 'error' };

  // 检查缓存
  if (DailyLoginRewardsCache && now.getTime() >= DailyLoginRewardsCache.lastScraped.getTime() && now.getTime() < DailyLoginRewardsCache.nextRefresh.getTime()) {
    console.log('使用 Daily Login Rewards 缓存数据:', DailyLoginRewardsCache.data);
    return DailyLoginRewardsCache.data;
  }

  let browser;
  try {
    const url = 'https://eso-hub.com/en/daily-login-rewards';
    let attempts = 0;
    const maxAttempts = 3;
    let html;

    while (attempts < maxAttempts) {
      attempts++;
      try {
        // 启动 Puppeteer
        browser = await puppeteer.launch({
          headless: true,
          args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security'],
          executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        });
        const page = await browser.newPage();

        // 设置 User-Agent 和视口
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36');
        await page.setViewport({ width: 1280, height: 800 });

        // 增加伪装
        await page.setExtraHTTPHeaders({
          'Accept-Language': 'en-US,en;q=0.9',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        });

        // 访问页面
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
        await page.waitForSelector('body', { timeout: 30000 });

        // 检查 Cloudflare
        const title = await page.title();
        if (title.includes('Just a moment') || title.includes('Access denied')) {
          throw new Error(`Cloudflare 拦截，标题: ${title}`);
        }

        // 等待网格加载
        await page.waitForSelector('div.grid', { timeout: 30000 });

        // 获取页面 HTML
        html = await page.content();
        break;
      } catch (error) {
        console.warn(`尝试 ${attempts} 失败: ${error.message}`);
        if (attempts === maxAttempts) throw error;
        if (browser) await browser.close().catch(() => {});
        await new Promise(resolve => setTimeout(resolve, 2000 * attempts));
      }
    }

    const $ = load(html);

    // 选择目标网格
    const grid = $('div.grid.grid-cols-3.md\\:grid-cols-7').eq(0);
    if (!grid.length) {
      console.warn('HTML 内容:', html.slice(0, 500));
      console.warn('所有网格类:', $('div.grid').map((i, el) => $(el).attr('class')).get());
      throw new Error('未找到每日登录奖励网格');
    }
    console.log(`找到目标网格，类: ${grid.attr('class')}`);

    const items = [];
    // 选择网格的直接子节点
    const itemDivs = grid.children('div').filter((i, el) => {
      const $el = $(el);
      return $el.find('img').length && $el.find('div.font-bold.text-2xs').length && $el.find('div.font-bold.text-xs').length;
    });
    if (itemDivs.length === 0) {
      console.warn('未找到奖励物品，网格 HTML:', grid.html().slice(0, 500));
      throw new Error('未找到每日登录奖励物品');
    }
    console.log(`找到 ${itemDivs.length} 个奖励物品`);

    // 收集所有物品数据
    const rowData = [];
    itemDivs.each((i, div) => {
      const $div = $(div);

      // 提取 day
      const dayText = $div.find('div.font-bold.text-xs.text-white').text().trim();
      const day = parseInt(dayText) || 'error';

      // 提取 icon
      const iconSrc = $div.find('img').attr('src') || 'error';
      let icon = 'error';
      if (iconSrc === '/images/telvar.png'){
        icon = 'telvar'
      } else if (iconSrc !== 'error') {
         const match = iconSrc.match(/\/storage\/icons\/(.+)\.(png|webp)$/);
         icon = match ? match[1] : 'error';
      }

      // 提取 enName
      const enName = $div.find('div.font-bold.text-2xs.text-white').text().trim() || 'error';

      // 提取 amount
      const amountText = $div.find('div.font-bold.text-white:not(.text-2xs):not(.text-xs)').text().trim();
      const amount = parseInt(amountText) || 'error';

      if (day !== 'error' && icon !== 'error' && enName !== 'error' && amount !== 'error') {
        rowData.push({ icon, enName, day, amount });
      } else {
        console.warn(`第 ${i + 1} 项数据无效，跳过: day=${day}, icon=${icon}, enName=${enName}, amount=${amount}`);
      }
    });

    // 批量查询 zhText
    for (const row of rowData) {
      try {
        const query = `
          SELECT zhText
          FROM esoText
          WHERE enText = ?
          ORDER BY id DESC
          LIMIT 1
        `;
        const [results] = await dataPool.query(query, [row.enName]);
        const zhName = results.length > 0 ? results[0].zhText : row.enName;
        items.push({ icon: row.icon, name: zhName, enName: row.enName, day: row.day, amount: row.amount });
      } catch (dbError) {
        console.warn(`查询 zhText 失败，enName=${row.enName}，使用英文名: ${dbError.message}`);
        items.push({ icon: row.icon, name: row.enName, enName: row.enName, day: row.day, amount: row.amount });
      }
    }

    if (items.length === 0) {
      console.warn('奖励物品数量为 0，网格 HTML:', grid.html().slice(0, 500));
      throw new Error('未找到每日登录奖励物品');
    }

    // 计算时间范围（当月）
    const lastRefresh = getLastMonthRefreshTime(now);
    const year = lastRefresh.getUTCFullYear();
    const month = lastRefresh.getUTCMonth() + 1;
    const time = `${year}年${month}月`;

    const data = { items, time };
    DailyLoginRewardsCache = {
      data,
      lastScraped: now,
      nextRefresh: getNextRefreshTime(now),
    };
    console.log('爬取 Daily Login Rewards 成功:', data, '下次刷新:', DailyLoginRewardsCache.nextRefresh.toISOString());

    return data;
  } catch (error) {
    console.error('爬取 Daily Login Rewards 失败:', error);
    return defaultData;
  } finally {
    if (browser) await browser.close().catch(err => console.warn('关闭浏览器失败:', err));
  }
}

// 一次性获取所有装备数据
app.get('/api/equipment/all', async (req, res) => {
  const query = `
    SELECT sets.*, 
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses
    FROM sets
    LEFT JOIN bonuses ON sets.id = bonuses.set_id
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
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses
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
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses
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
});

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
  getNews();
  const query = `
    SELECT id, name, des, date, cover 
    FROM newsList
    ORDER BY sortID ASC
  `;

  try {
    const [rows] = await newsPool.query(query);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/top-news', async (req, res) => {
  getNews();
  try {
    const data = await fs.readFile('./src/Data/top-news.txt', 'utf8');
    res.json({ data: data.trim() }); // 使用trim()移除可能的换行符
  } catch (err) {
    console.log("获取顶部元素失败")
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

app.get('/api/Luxury-Furnisher', async (req, res) => {
  const data = await scrapeLuxuryFurnisher();
  res.json({
    data: data.items,
    timestamp: data.timestamp,
  });
});

app.get('/api/tel-var-vendor', async (req, res) => {
  const data = await scrapeTelVarVendor();
  res.json({
    data: data.items,
    time: data.time,
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

// 新增：获取 Filer Ool 数据
app.get('/api/infinite-vendor', async (req, res) => {
  const data = await scrapeInfiniteVendor();
  res.json({
    data: data.items,
    time: data.time,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/daily-login-rewards', async (req, res) => {
  const data = await scrapeDailyLoginRewards();
  res.json({
    data: data.items,
    time: data.time,
    timestamp: new Date().toISOString()
  });
});

// 启动服务器
app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});