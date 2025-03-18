// 后端API服务器
import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';
import {load} from 'cheerio'
import fetch from 'node-fetch'
import { transformWithEsbuild } from 'vite';


const app = express();
app.use(cors()); // 启用 CORS


// 创建数据库连接池
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root', // 替换为你的 MySQL 用户名
  password: 'Lzr@136595755', // 替换为你的 MySQL 密码
  database: 'eso_equipment',
  waitForConnections: true,
  connectionLimit: 10, // 连接池大小
  queueLimit: 0,
});

const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_skills',
};

const PledgeList1 = [
  "Spindleclutch II",
  "The Banished Cells I",
  "Fungal Grotto II",
  "Spindleclutch I",
  "Darkshade Caverns II",
  "Elden Hollow I",
  "Wayrest Sewers II",
  "Fungal Grotto I",
  "The Banished Cells II",
  "Darkshade Caverns I",
  "Elden Hollow II",
  "Wayrest Sewers I"
];

const PledgeList2 = [
  "Direfrost Keep",
  "Vaults of Madness",
  "Crypt of Hearts II",
  "City of Ash I",
  "Tempest Island",
  "Blackheart Haven",
  "Arx Corinium",
  "Selene's Web",
  "City of Ash II",
  "Crypt of Hearts I",
  "Volenfell",
  "Blessed Crucible"
];

const PledgeList3 = [
  "Imperial City Prison",
  "Ruins of Mazzatun",
  "White-Gold Tower",
  "Cradle of Shadows",
  "Bloodroot Forge",
  "Falkreath Hold",
  "Fang Lair",
  "Scalecaller Peak",
  "Moon Hunter Keep",
  "March of Sacrifices",
  "Depths of Malatar",
  "Frostvault",
  "Moongrave Fane",
  "Lair of Maarselok",
  "Icereach",
  "Unhallowed Grave",
  "Stone Garden",
  "Castle Thorn",
  "Black Drake Villa",
  "The Cauldron",
  "Red Petal Bastion",
  "The Dread Cellar",
  "Coral Aerie",
  "Shipwright's Regret",
  "Earthen Root Enclave",
  "Graven Deep"
];

//计算无畏者更新
function getDailyPledges() {
  const startIndex1 = PledgeList1.indexOf("Spindleclutch I");
  const startIndex2 = PledgeList2.indexOf("City of Ash I");
  const startIndex3 = PledgeList3.indexOf("Imperial City Prison");

  const now = new Date();
  
  const startDate = new Date('2025-03-12T18:00:00');

  const timeDiff = now.getTime() - startDate.getTime();
  const hoursDiff = timeDiff / (1000 * 3600);
  const daysDiff = Math.floor(hoursDiff / 24);
  let rotationCount = daysDiff;
  rotationCount -- ;
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

async function scrapeServerStatus() {
  try {
    const statusList = {
      "PCEU": "",
      "PCNA": "",
      "PCPTS": "",
      "XBOXEU": "",
      "XBOXNA": "",
      "PSEU": "",
      "PSNA": "",
    };
    let url = 'https://esoserverstatus.net/' ;
    let res = await fetch(url)
    let statusData = await res.text()
    //PC美服
    var tempData = statusData.split('PC-NA')[1].split('PC-PTS')[0].split('<b>')[1].split('</b>')[0];
    statusList.PCNA = tempData;
    //PC欧服
    var tempData = statusData.split('PC-EU')[1].split('PC-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.PCEU = tempData;
    //PC测试服
    var tempData = statusData.split('PC-PTS')[1].split('XBOX-EU')[0].split('<b>')[1].split('</b>')[0];
    statusList.PCPTS = tempData;
    //XBOX欧服
    var tempData = statusData.split('XBOX-EU')[1].split('XBOX-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.XBOXEU = tempData;
    //XBOX美服
    var tempData = statusData.split('XBOX-NA')[1].split('PS4-EU')[0].split('<b>')[1].split('</b>')[0];
    statusList.XBOXNA= tempData;
    //PS4欧服
    var tempData = statusData.split('PS4-EU')[1].split('PS4-NA')[0].split('<b>')[1].split('</b>')[0];
    statusList.PSEU= tempData;
    //PS5美服
    var tempData = statusData.split('PS4-NA')[1].split('/span')[0].split('<b>')[1].split('</b>')[0];
    statusList.PSNA= tempData;
    return statusList
  } catch (error) {
    console.error('爬取服务器状态失败:', error);
    return Array(7).fill('error');
  }
}

// 一次性获取所有装备数据（包括 bonuses 和 styles）
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
    const [rows] = await pool.query(query); // 查询所有数据
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 分页查询套装列表（保留原有逻辑）
app.get('/api/equipment', async (req, res) => {
  const { page = 1, limit = 20 } = req.query;
  const offset = (page - 1) * limit;

  const query = `
    SELECT * FROM sets
    ORDER BY id desc
    LIMIT ? OFFSET ?
  `;
  const values = [parseInt(limit), parseInt(offset)];

  try {
    const [sets] = await pool.query(query, values); // 使用 pool.query
    res.json(sets);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/equipment/related/:place', async (req, res) => {
  const { place } = req.params;
  const formattedPlace = decodeURIComponent(place).trim(); // 去掉多余空格
  const hexPlace = Buffer.from(formattedPlace, 'utf8').toString('hex').toUpperCase(); // 转换为十六进制

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
    const [rows] = await pool.query(query, [hexPlace]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 根据 enName 查询套装详情（保留原有逻辑）
app.get('/api/equipment/:enName', async (req, res) => {
  const { enName } = req.params;
  const formattedEnName = decodeURIComponent(enName.replace(/_/g, '%20')); // 将下划线替换为空格

  const query = `
    SELECT sets.*, 
           JSON_OBJECTAGG(bonuses.effect_key, bonuses.effect_value) AS bonuses,
           (SELECT JSON_ARRAYAGG(styles.icon) 
            FROM styles 
            WHERE styles.set_id = sets.id) AS styles
    FROM sets
    LEFT JOIN bonuses ON sets.id = bonuses.set_id
    WHERE sets.enName = ?
    GROUP BY sets.id;
  `;

  try {
    const [rows] = await pool.query(query, [formattedEnName]); // 使用 pool.query

    if (rows.length === 0) {
      return res.status(404).json({ error: '未找到套装' });
    }

    res.json(rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 获取所有技能数据
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

// API 端点
app.get('/api/daily-pledges', (req, res) => {
  const result = getDailyPledges();
  res.json(result);
});

app.get('/api/server-status', async (req, res) => {
  const statusList = await scrapeServerStatus();
  res.json({
    status: statusList,
    timestamp: new Date().toISOString()
  });
});

// 启动服务器
app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});