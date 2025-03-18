import json
import pymysql

# 连接 MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Lzr@136595755",
    database="eso_skills",
    charset="utf8mb4"
)
cursor = conn.cursor()

# 其余代码保持不变

# 加载 JSON 数据
with open("C:/projects/ESOCN/src/Data/skills.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 插入数据
for class_data in data:
    # 插入 classes 表
    cursor.execute("INSERT IGNORE INTO classes (name, enName) VALUES (%s, %s)",
                   (class_data["name"], class_data["enName"]))
    class_id = cursor.lastrowid

    # 遍历技能树 (data)
    for skill_tree in class_data.get("data", []):
        # 插入 skill_trees 表
        cursor.execute("INSERT IGNORE INTO skill_trees (class_id, name, enName) VALUES (%s, %s, %s)",
                       (class_id, skill_tree["name"], skill_tree["enName"]))
        skill_tree_id = cursor.lastrowid

        # 遍历技能 (skills)
        for skill in skill_tree.get("skills", []):
            # 处理 icon，将 .dds 替换为 .webp
            base_icon = skill.get("icon", "")
            if base_icon and base_icon.endswith(".dds"):
                base_icon = base_icon[:-4] + ".webp"

            # 插入 skills 表（基础技能）
            cursor.execute("""
                INSERT IGNORE INTO skills (skill_tree_id, name, description, isChanneled,
                                    ultimate, cost, duration, castTime, maxRange, minRange, 
                                    radius, target, icon, enName, passive, newEffect, 
                                    magickaCost, staminaCost, healthCost)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (skill_tree_id, skill["name"], skill.get("description"), skill.get("isChanneled"),
                  skill.get("ultimate"), skill.get("cost"), skill.get("duration"), skill.get("castTime"), skill.get("maxRange"),
                  skill.get("minRange"), skill.get("radius"), skill.get("target"), base_icon, skill.get("enName"), 
                  skill.get("passive"), "", skill['powerTypes'].get("magickaCost"), skill['powerTypes'].get("staminaCost"),
                  skill['powerTypes'].get("healthCost")))

            skill_id = cursor.lastrowid

            # 遍历技能变体 (data)
            for variant in skill.get("data", []):
                variant_icon = variant.get("icon", "")
                if variant_icon and variant_icon.endswith(".dds"):
                    variant_icon = variant_icon[:-4] + ".webp"

                # 插入 skill_variants 表（技能变体）
                cursor.execute("""
                    INSERT IGNORE INTO skill_variants (skill_id, name, description, newEffect, cost, duration, castTime,
                                               maxRange, minRange, radius, target, icon, enName, passive, ultimate, 
                                                isChanneled, magickaCost, staminaCost, healthCost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (skill_id, variant["name"], variant.get("description"), variant.get("newEffect"),
                      variant.get("cost"), variant.get("duration"), variant.get("castTime"),
                      variant.get("maxRange"), variant.get("minRange"), variant.get("radius"),
                      variant.get("target"), variant_icon, variant.get("enName"), variant.get("passive"), 
                      variant.get("ultimate"), variant.get("isChanneled"), variant['powerTypes'].get("magickaCost"),
                      variant['powerTypes'].get("staminaCost"), variant['powerTypes'].get("healthCost")))

# 提交事务
conn.commit()
cursor.close()
conn.close()

print("数据插入完成！")