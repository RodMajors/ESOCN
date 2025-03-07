import fs from 'fs';
import mysql from 'mysql2';

// 读取 JSON 文件
const equipmentData = JSON.parse(fs.readFileSync('./src/Data/equipment.json', 'utf8'));

// 创建数据库连接
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root', // 替换为你的 MySQL 用户名
  password: 'Lzr@136595755', // 替换为你的 MySQL 密码
  database: 'eso_equipment',
});

// 连接数据库
connection.connect();

// 插入套装数据
const insertSets = async () => {
  for (const set of equipmentData.sets) {
    // 插入套装数据
    const query = `
      INSERT IGNORE INTO sets (id, name, enName, place, enplace, type, icon, style, armor)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    const values = [set.id, set.name, set.enName, set.place, set.enplace, set.type, set.icon, set.style, set.armor];
    await connection.promise().query(query, values);

    // 插入套装效果
    for (const [key, value] of Object.entries(set.bonuses)) {
      if (value) {
        const query = `
          INSERT IGNORE INTO bonuses (set_id, effect_key, effect_value)
          VALUES (?, ?, ?)
        `;
        const values = [set.id, key, value];
        await connection.promise().query(query, values);
      }
    }

    // 插入样式
    for (const [category, subCategories] of Object.entries(set.styles)) {
      for (const [subCategory, styles] of Object.entries(subCategories)) {
        for (const [styleName, styleData] of Object.entries(styles)) {
          const query = `
            INSERT IGNORE INTO styles (set_id, category, sub_category, style, style_id, icon)
            VALUES (?, ?, ?, ?, ?, ?)
          `;
          const values = [
            set.id,
            category,
            subCategory,
            styleData.style,
            styleData.styleId,
            styleData.icon,
          ];
          await connection.promise().query(query, values);
        }
      }
    }
  }
  console.log('数据导入完成');
  connection.end();
};

insertSets().catch(err => console.error(err));