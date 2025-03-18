import express from 'express'
import mysql from 'mysql2/promise'
import cors from 'cors'; // 新增
const app = express();
const port = 4000;

// MySQL 连接配置
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: 'Lzr@136595755',
  database: 'eso_skills',
};

// 中间件
app.use(express.json());
app.use(cors()); // 添加 CORS 中间件

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

// 启动服务器
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});