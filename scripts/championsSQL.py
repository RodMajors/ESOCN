import json
import mysql.connector
from mysql.connector import Error
import re

def connect_to_database():
    """连接到MySQL数据库"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lzr@136595755",
            database="esocp"
        )
        if connection.is_connected():
            print("成功连接到MySQL数据库")
            return connection
    except Error as e:
        print(f"连接数据库时出错: {e}")
        return None

def create_table(connection):
    """创建cp_skills表"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS cp_skills (
            id INT PRIMARY KEY,
            category_id INT,
            category_name VARCHAR(50),
            skill_index INT,
            name VARCHAR(100),
            en_name VARCHAR(100),
            description TEXT,
            is_slottable BOOLEAN,
            cluster_name VARCHAR(50),
            bonus_text JSON,
            is_in_cluster BOOLEAN,
            type INT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("成功创建或确认cp_skills表")
    except Error as e:
        print(f"创建表时出错: {e}")
    finally:
        cursor.close()

def split_skill_name(full_name):
    """将技能名称拆分为中文和英文"""
    match = re.match(r'^(.*?)\s*\((.*?)\)$', full_name.strip())
    if match:
        cn_name = match.group(1).strip()
        en_name = match.group(2).strip()
        return cn_name, en_name
    return full_name.strip(), ""

def insert_skills(connection, skills_data):
    """将dataCpSkills数据插入数据库"""
    try:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO cp_skills (
            id, category_id, category_name, skill_index, name, 
            en_name, description, is_slottable, cluster_name, 
            bonus_text, is_in_cluster, type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            category_id = VALUES(category_id),
            category_name = VALUES(category_name),
            skill_index = VALUES(skill_index),
            name = VALUES(name),
            en_name = VALUES(en_name),
            description = VALUES(description),
            is_slottable = VALUES(is_slottable),
            cluster_name = VALUES(cluster_name),
            bonus_text = VALUES(bonus_text),
            is_in_cluster = VALUES(is_in_cluster),
            type = VALUES(type);
        """
        
        # 遍历dataCpSkills的values，而不是keys
        for category in skills_data.values():
            category_id = category.get('id')
            category_name = category.get('name')
            print(f"处理类别: {category_name} (ID: {category_id})")
            
            # 将skills字典转换为列表
            skills = list(category.get('skills', {}).values())
            if not skills:
                print(f"警告: 类别 {category_name} 中没有技能数据")
                continue
                
            for skill in skills:
                cn_name, en_name = split_skill_name(skill['name'])
                bonus_text = json.dumps(skill.get('bounsText', {}))
                skill_data = (
                    skill['id'],
                    category_id,
                    category_name,
                    skill['index'],
                    cn_name,
                    en_name,
                    skill['description'],
                    skill['isSlottable'],
                    skill['clusterName'],
                    bonus_text,
                    skill['isInCluster'],
                    skill['type']
                )
                cursor.execute(insert_query, skill_data)
        
        connection.commit()
        print("成功插入技能数据")
    except Error as e:
        print(f"插入数据时出错: {e}")
    finally:
        cursor.close()

def main():
    json_file_path = "C:/projects/ESOCN/public/data/DataExtractor.json"
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            skills_data = data['Default']['@RodMajors']['$AccountWide']['dataCpSkills']
            print(f"skills_data 类型: {type(skills_data)}")
            print(f"skills_data 键: {list(skills_data.keys())}")
    except Exception as e:
        print(f"读取JSON文件时出错: {e}")
        return
    
    connection = connect_to_database()
    if not connection:
        return
    
    create_table(connection)
    insert_skills(connection, skills_data)
    
    if connection.is_connected():
        connection.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    main()