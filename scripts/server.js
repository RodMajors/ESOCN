import express from 'express';
import mysql from 'mysql2/promise';
import cors from 'cors';

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

// 启动服务器
app.listen(3000, () => {
  console.log('服务器运行在 http://localhost:3000');
});