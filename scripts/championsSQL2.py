import json
import mysql.connector
from mysql.connector import Error

def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def connect_to_database():
    """连接到 MySQL 数据库"""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # 替换为你的数据库主机
            database='esocp',  # 替换为你的数据库名称
            user='root',  # 替换为你的数据库用户名
            password='Lzr@136595755'  # 替换为你的数据库密码
        )
        if connection.is_connected():
            print("成功连接到 MySQL 数据库")
            return connection
    except Error as e:
        print(f"连接数据库时出错: {e}")
        return None

def update_skills_in_db(connection, skills):
    """更新 cp_skills 表中的技能数据，包含新字段"""
    cursor = connection.cursor()
    
    # SQL 更新语句，包含 max_points 等新字段
    sql = """
    INSERT INTO cp_skills (
        id, skill_index, name, en_name, description,
        is_slottable, cluster_name, bonus_text, is_in_cluster, type,
        max_points, jump_points, num_jump_points, jump_point_delta
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        skill_index = VALUES(skill_index),
        name = VALUES(name),
        en_name = VALUES(en_name),
        description = VALUES(description),
        is_slottable = VALUES(is_slottable),
        cluster_name = VALUES(cluster_name),
        bonus_text = VALUES(bonus_text),
        is_in_cluster = VALUES(is_in_cluster),
        type = VALUES(type),
        max_points = VALUES(max_points),
        jump_points = VALUES(jump_points),
        num_jump_points = VALUES(num_jump_points),
        jump_point_delta = VALUES(jump_point_delta)
    """
    
    for skill in skills:
        # 映射 JSON 字段到数据库字段
        data = (
            skill.get('id'),
            skill.get('index'),
            skill.get('name'),
            skill.get('enName'),
            skill.get('description'),
            skill.get('isSlottable'),
            skill.get('clusterName'),
            json.dumps(skill.get('bounsText', {})),  # 转换为 JSON 字符串
            skill.get('isInCluster'),
            skill.get('type'),
            int(skill.get('maxPoints')) if skill.get('maxPoints') else None,  # 转换为 INT
            skill.get('jumpPoints'),
            int(skill.get('numJumpPoints')) if skill.get('numJumpPoints') else None,  # 转换为 INT
            int(skill.get('jumpPointDelta')) if skill.get('jumpPointDelta') else None  # 转换为 INT
        )
        
        try:
            cursor.execute(sql, data)
        except Error as e:
            print(f"更新技能 ID {skill.get('id')} 时出错: {e}")
    
    connection.commit()
    print(f"成功更新 {cursor.rowcount} 条记录")

def main():
    # 加载 JSON 文件
    data = load_json('C:/projects/ESOCN/public/data/merged_skills.json')
    skills = data.get('skills', [])
    
    # 连接数据库
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        # 更新技能数据
        update_skills_in_db(connection, skills)
    except Error as e:
        print(f"更新数据时出错: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("数据库连接已关闭")

if __name__ == '__main__':
    main()