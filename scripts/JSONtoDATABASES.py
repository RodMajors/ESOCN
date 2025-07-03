import json
import re
import mysql.connector
from mysql.connector import Error
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def connect_to_database(database_name):
    """连接到 MySQL 数据库"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Lzr@136595755',
            database=database_name,
            charset='utf8mb4'
        )
        logger.info(f"Successfully connected to database '{database_name}'")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Failed to connect to database '{database_name}': {err}")
        raise

def get_power_type_values(power_types):
    """从 powerTypes 数组提取 magickaCost, staminaCost, healthCost"""
    magicka_cost = 0
    stamina_cost = 0
    health_cost = 0
    if isinstance(power_types, list):
        for pt in power_types:
            if isinstance(pt, dict):
                magicka_cost = pt.get('magickaCost', magicka_cost)
                stamina_cost = pt.get('staminaCost', stamina_cost)
                health_cost = pt.get('healthCost', health_cost)
    return magicka_cost, stamina_cost, health_cost

def insert_equipment_data(connection, equipment_data):
    """将 equipment.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_sets = 0
    inserted_bonuses = 0
    try:
        for set_item in equipment_data.get('equipment', []):
            # 插入套装数据到 sets 表，包括 styles 作为 JSON
            set_query = """
                INSERT IGNORE INTO sets (id, name, enName, place, enplace, type, icon, style, armor, styles)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            set_values = (
                set_item['id'],
                set_item['name'],
                set_item['enName'],
                set_item['place'],
                set_item['enplace'],
                set_item['type'],
                set_item['icon'],
                set_item['style'],
                set_item['armor'],
                json.dumps(set_item.get('styles', {}))  # 序列化 styles 为 JSON 字符串
            )
            cursor.execute(set_query, set_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped set (possible duplicate): id={set_item['id']}, name={set_item['name']}")
            else:
                logger.debug(f"Inserted set: id={set_item['id']}, name={set_item['name']}")
            inserted_sets += cursor.rowcount

            # 插入套装效果到 bonuses 表
            for effect_key, effect_value in set_item.get('bonuses', {}).items():
                if effect_value:
                    bonus_query = """
                        INSERT IGNORE INTO bonuses (set_id, effect_key, effect_value)
                        VALUES (%s, %s, %s)
                    """
                    bonus_values = (set_item['id'], effect_key, effect_value)
                    cursor.execute(bonus_query, bonus_values)
                    inserted_bonuses += cursor.rowcount

        connection.commit()
        logger.info(f"Equipment import completed: {inserted_sets} sets, {inserted_bonuses} bonuses inserted")
    except Exception as e:
        logger.error(f"Error during equipment import: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def insert_skills_data(connection, skills_data):
    """将 skills.json 数据插入数据库"""
    cursor = connection.cursor(buffered=True)  # 使用 buffered 游标避免 Unread result found
    inserted_classes = 0
    inserted_skill_trees = 0
    inserted_skills = 0
    inserted_variants = 0

    try:
        # 用于缓存 typeName 和 categoryName 的 ID
        class_cache = {}  # typeName -> class_id
        skill_tree_cache = {}  # (class_id, categoryName) -> skill_tree_id

        for skill_item in skills_data.get('skills', []):
            if not skill_item.get('name'):
                logger.warning(f"Skipping skill with empty name, id: {skill_item.get('id')}")
                continue

            type_name = skill_item.get('typeName', '')
            type_en_name = skill_item.get('typeEnName', type_name)
            category_name = skill_item.get('categoryName', '')
            category_en_name = skill_item.get('categoryEnName', category_name)

            # 插入或获取 classes 表中的职业
            if type_name not in class_cache:
                class_query = """
                    INSERT IGNORE INTO classes (name, enName)
                    VALUES (%s, %s)
                """
                cursor.execute(class_query, (type_name, type_en_name))
                if cursor.rowcount > 0:
                    inserted_classes += 1
                # 获取 class_id
                cursor.execute("SELECT id FROM classes WHERE name = %s", (type_name,))
                class_id = cursor.fetchone()[0]
                class_cache[type_name] = class_id
            else:
                class_id = class_cache[type_name]

            # 插入或获取 skill_trees 表中的技能树
            skill_tree_key = (class_id, category_name)
            if skill_tree_key not in skill_tree_cache:
                skill_tree_query = """
                    INSERT IGNORE INTO skill_trees (class_id, name, enName)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(skill_tree_query, (class_id, category_name, category_en_name))
                if cursor.rowcount > 0:
                    inserted_skill_trees += 1
                # 获取 skill_tree_id
                cursor.execute("SELECT id FROM skill_trees WHERE class_id = %s AND name = %s",
                              (class_id, category_name))
                skill_tree_id = cursor.fetchone()[0]
                skill_tree_cache[skill_tree_key] = skill_tree_id
            else:
                skill_tree_id = skill_tree_cache[skill_tree_key]

            # 处理图标
            base_icon = skill_item.get('icon', '')
            if base_icon.endswith('.dds'):
                base_icon = base_icon[:-4] + '.webp'

            # 提取 powerTypes
            magicka_cost, stamina_cost, health_cost = get_power_type_values(skill_item.get('powerTypes', []))

            # 插入 skills 表（基础技能）
            skill_query = """
                INSERT IGNORE INTO skills (
                    skill_tree_id, name, enName, description, isChanneled,
                    ultimate, cost, duration, castTime, maxRange, minRange,
                    radius, target, icon, passive, newEffect,
                    magickaCost, staminaCost, healthCost
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            skill_values = (
                skill_tree_id,
                skill_item.get('name', ''),
                skill_item.get('enName', skill_item.get('name', '')),
                skill_item.get('description', ''),
                skill_item.get('isChanneled', False),
                skill_item.get('ultimate', False),
                skill_item.get('cost', 0),
                skill_item.get('duration', 0),
                skill_item.get('castTime', 0),
                skill_item.get('maxRange', 0),
                skill_item.get('minRange', 0),
                skill_item.get('radius', 0),
                skill_item.get('target', ''),
                base_icon,
                skill_item.get('passive', False),
                skill_item.get('newEffect', ''),
                magicka_cost,
                stamina_cost,
                health_cost
            )
            try:
                cursor.execute(skill_query, skill_values)
                if cursor.rowcount > 0:
                    inserted_skills += 1
                # 获取 skill_id
                cursor.execute("SELECT id FROM skills WHERE skill_tree_id = %s AND name = %s",
                              (skill_tree_id, skill_item.get('name', '')))
                skill_id = cursor.fetchone()[0]
            except mysql.connector.Error as err:
                logger.error(f"Failed to insert skill '{skill_item.get('name')}': {err}")
                logger.debug(f"Skill query: {skill_query}")
                logger.debug(f"Skill values: {skill_values}")
                raise

            # 插入技能变体
            for variant in skill_item.get('advance', []):
                variant_icon = variant.get('icon', '')
                if variant_icon.endswith('.dds'):
                    variant_icon = variant_icon[:-4] + '.webp'

                variant_magicka_cost, variant_stamina_cost, variant_health_cost = get_power_type_values(variant.get('powerTypes', []))

                variant_query = """
                    INSERT IGNORE INTO skill_variants (
                        skill_id, name, enName, description, newEffect, cost, duration, castTime,
                        maxRange, minRange, radius, target, icon, passive, ultimate,
                        isChanneled, magickaCost, staminaCost, healthCost
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                variant_values = (
                    skill_id,
                    variant.get('name', ''),
                    variant.get('enName', variant.get('name', '')),
                    variant.get('description', ''),
                    variant.get('newEffect', ''),
                    variant.get('cost', 0),
                    variant.get('duration', 0),
                    variant.get('castTime', 0),
                    variant.get('maxRange', 0),
                    variant.get('minRange', 0),
                    variant.get('radius', 0),
                    variant.get('target', ''),
                    variant_icon,
                    variant.get('passive', False),
                    variant.get('ultimate', False),
                    variant.get('isChanneled', False),
                    variant_magicka_cost,
                    variant_stamina_cost,
                    variant_health_cost
                )
                try:
                    cursor.execute(variant_query, variant_values)
                    inserted_variants += cursor.rowcount
                except mysql.connector.Error as err:
                    logger.error(f"Failed to insert variant '{variant.get('name')}': {err}")
                    logger.debug(f"Variant query: {variant_query}")
                    logger.debug(f"Variant values: {variant_values}")
                    raise

        connection.commit()
        logger.info(f"Skills import completed: {inserted_classes} classes, {inserted_skill_trees} skill trees, {inserted_skills} skills, {inserted_variants} variants inserted")

    except mysql.connector.Error as err:
        logger.error(f"Database error during skills insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in skills insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def insert_furniture_data(connection, furniture_data):
    """将 furniture.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_furniture = 0

    try:
        for furniture_item in furniture_data.get('furniture', []):
            ingredients = {}
            skills = {}
            #处理ingredients
            pattern = re.compile(r'([^(),]+)\s*\(\s*(\d+)\s*\)')
            matches = pattern.finditer(furniture_item['ingredients'])
            for match in matches:
                name = match.group(1).strip()
                quantity = int(match.group(2))
                ingredients[name] = quantity
                
            pattern = re.compile(r'([^\d]+)\s+(\d+)')
            matches = pattern.finditer(furniture_item['skills'])
            for match in matches:
                name = match.group(1).strip()
                quantity = int(match.group(2))
                skills[name] = quantity
                
            # 插入套装数据到 furniture 表
            furniture_query = """
                INSERT IGNORE INTO furniture (id, name, enName, icon, type,
                quality, description, canBeCrafted, category, subCategory,
                ingredients, skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            set_values = (
                furniture_item['id'],
                furniture_item['name'],
                furniture_item['enName'],
                furniture_item['icon'],
                furniture_item['type'],
                furniture_item['quality'],
                furniture_item['description'],
                furniture_item['canBeCrafted'],
                furniture_item['category'],
                furniture_item['subCategory'],
                json.dumps(ingredients, ensure_ascii=False),
                json.dumps(skills, ensure_ascii=False),
            )
            cursor.execute(furniture_query, set_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped set (possible duplicate): id={furniture_item['id']}, name={furniture_item['name']}")
            else:
                logger.debug(f"Inserted set: id={furniture_item['id']}, name={furniture_item['name']}")
            inserted_furniture += cursor.rowcount

        connection.commit()
        logger.info(f"furniture import completed: {inserted_furniture} furniture, ")

    except mysql.connector.Error as err:
        logger.error(f"Database error during furniture insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in furniture insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        
def insert_collectibleFurniture_data(connection, furniture_data):
    """将 furniture.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_furniture = 0

    try:
        for furniture_item in furniture_data.get('collectibleFurniture', []):
            # 插入套装数据到 furniture 表
            furniture_query = """
                INSERT IGNORE INTO collectibleFurniture (id, name, enName, icon, 
                furnitureId, quality, description,  category, hint)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            set_values = (
                furniture_item['id'],
                furniture_item['name'],
                furniture_item['enName'],
                furniture_item['icon'],
                furniture_item['furnitureId'],
                furniture_item['quality'],
                furniture_item['description'],
                furniture_item['category'],
                furniture_item['hint'],
            )
            cursor.execute(furniture_query, set_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped set (possible duplicate): id={furniture_item['id']}, name={furniture_item['name']}")
            else:
                logger.debug(f"Inserted set: id={furniture_item['id']}, name={furniture_item['name']}")
            inserted_furniture += cursor.rowcount

        connection.commit()
        logger.info(f"collectibleFurniture import completed: {inserted_furniture} collectibleFurniture, ")

    except mysql.connector.Error as err:
        logger.error(f"Database error during collectibleFurniture insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in collectibleFurniture insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        
def insert_cpSkills_data(connection, skills):
    """更新 cp_skills 表中的技能数据，包含新字段"""
    cursor = connection.cursor()
    
    # SQL 更新语句，包含 max_points 等新字段
    sql = """
    INSERT IGNORE INTO cp_skills (
        id, category_id, category_name, skill_index, name, en_name, description,
        is_slottable, cluster_name, bonus_text, is_in_cluster, type,
        max_points, jump_points, num_jump_points, jump_point_delta
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        type = VALUES(type),
        max_points = VALUES(max_points),
        jump_points = VALUES(jump_points),
        num_jump_points = VALUES(num_jump_points),
        jump_point_delta = VALUES(jump_point_delta)
    """
    
    for skill in skills:
        categroy = ""
        is_slottable = False
        is_in_cluster = False
        if (skill.get('categoryId') == "1"):
            categroy = "战争"
        if (skill.get('categoryId') == "2"):
            categroy = "强健"
        if (skill.get('categoryId') == "3"):
            categroy = "制作"
        if (skill.get('isSlottable') == "True"):
            is_slottable = True
        if (skill.get('isInCluster') == "True"):
            is_in_cluster = True
        # 映射 JSON 字段到数据库字段
        data = (
            skill.get('id'),
            skill.get('categoryId'),
            categroy,
            skill.get('index'),
            skill.get('name'),
            skill.get('enName'),
            skill.get('description'),
            is_slottable,
            skill.get('clusterName'),
            json.dumps(skill.get('bounsText', {})),  # 转换为 JSON 字符串
            is_in_cluster,
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
    
def insert_buffs_data(connection, buffs_data):
    """将 buffs.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_buffs = 0

    try:
        for buffs_item in buffs_data.get('buffs', []):
            # 插入套装数据到 sets 表
            buffs_query = """
                INSERT IGNORE INTO buffs (name, enName, des)
                VALUES (%s, %s, %s)
            """
            buff_values = (
                buffs_item['name'],
                buffs_item['enName'],
                buffs_item['des'],
            )
            cursor.execute(buffs_query, buff_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped buffs (possible duplicate): name={buffs_item['name']}")
            else:
                logger.debug(f"Inserted buffs name={buffs_item['name']}")
            inserted_buffs += cursor.rowcount
            
        for buffs_item in buffs_data.get('debuffs', []):
            # 插入套装数据到 buffs 表
            buffs_query = """
                INSERT IGNORE INTO debuffs (name, enName, des)
                VALUES (%s, %s, %s)
            """
            buff_values = (
                buffs_item['name'],
                buffs_item['enName'],
                buffs_item['des'],
            )
            cursor.execute(buffs_query, buff_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped buffs (possible duplicate): name={buffs_item['name']}")
            else:
                logger.debug(f"Inserted buffs name={buffs_item['name']}")
            inserted_buffs += cursor.rowcount


        connection.commit()
        logger.info(f"buff import completed: {inserted_buffs} buff, ")

    except mysql.connector.Error as err:
        logger.error(f"Database error during buff insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in buff insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def insert_foods_data(connection, foods_data):
    """将 foods.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_foods = 0

    try:
        for foods_item in foods_data.get('foods', []):
            canBeCrafted = False
            ingredients = {}
            if foods_item['canBeCrafted'] == "True":
                canBeCrafted = True

            #处理ingredients
            pattern = re.compile(r'([^(),]+)\s*\(\s*(\d+)\s*\)')
            matches = pattern.finditer(foods_item['ingredients'])
            for match in matches:
                name = match.group(1).strip()
                quantity = int(match.group(2))
                ingredients[name] = quantity

            # 插入套装数据到 foods 表
            foods_query = """
                INSERT IGNORE INTO foods (id, name, enName, ingredients, icon, itemTypeText, quality,
                description, canBeCrafted, specializedItemTypeText
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            foods_values = (
                int(foods_item['id']),
                foods_item['name'],
                foods_item['enName'],
                json.dumps(ingredients, ensure_ascii=False),
                foods_item['icon'],
                foods_item['itemTypeText'],
                foods_item['quality'],
                foods_item['description'],
                canBeCrafted,
                foods_item['specializedItemTypeText'],
            )
            cursor.execute(foods_query, foods_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped foods (possible duplicate): name={foods_item['name']}")
            else:
                logger.debug(f"Inserted foods name={foods_item['name']}")
            inserted_foods += cursor.rowcount
        connection.commit()
        logger.info(f"foods import completed: {inserted_foods} buff, ")

    except mysql.connector.Error as err:
        logger.error(f"Database error during foods insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in foods insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        
def insert_news_data(connection, news_data):
    """将 news.json 数据插入数据库"""
    cursor = connection.cursor()
    inserted_news = 0

    try:
        for news_item in news_data:
            # 插入新闻数据到 news 表
            news_query = """
                INSERT IGNORE INTO newsList (id, name, des, date, cover)
                VALUES (%s, %s, %s, %s, %s)
            """
            news_values = (
                news_item['id'],
                news_item['name'],
                news_item['des'],
                news_item['date'],
                news_item['cover']
            )
            cursor.execute(news_query, news_values)
            if cursor.rowcount == 0:
                logger.debug(f"Skipped news (possible duplicate): id={news_item['id']}, name={news_item['name']}")
            else:
                logger.debug(f"Inserted news: id={news_item['id']}, title={news_item['name']}")
            inserted_news += cursor.rowcount

        connection.commit()
        logger.info(f"News import completed: {inserted_news} items inserted")

    except mysql.connector.Error as err:
        logger.error(f"Database error during news insertion: {err}")
        connection.rollback()
        raise
    except Exception as err:
        logger.error(f"Unexpected error in news insertion: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def process_equipment_json(json_path):
    """处理 equipment.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('eso_equipment')
        try:
            # 插入数据
            insert_equipment_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for equipment")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing equipment.json: {err}")
        raise

def process_skills_json(json_path):
    """处理 skills.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('eso_skills')
        try:
            # 插入数据
            insert_skills_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for skills")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing skills.json: {err}")
        raise
    
def process_furniture_json(json_path):
    """处理 furniture.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('eso_furniture')
        try:
            # 插入数据
            insert_furniture_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for furniture")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing furniture.json: {err}")
        raise
    
def process_collectibleFurniture_json(json_path):
    """处理 furniture.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('eso_furniture')
        try:
            # 插入数据
            insert_collectibleFurniture_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for furniture")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing furniture.json: {err}")
        raise
    
def process_cpSkills_json(json_path):
    """处理 cpSkills.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f).get('skills', [])
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('esocp')
        try:
            # 插入数据
            insert_cpSkills_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for cpSkills")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing cpSkills.json: {err}")
        raise
    
def process_buffs_json(json_path):
    """处理 buffs.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('buffs')
        try:
            # 插入数据
            insert_buffs_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for buffs")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing buffs.json: {err}")
        raise

def process_foods_json(json_path):
    """处理 foods.json 文件并导入数据库"""
    try:
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded JSON file: {json_path}")

        # 连接数据库
        connection = connect_to_database('eso_foods')
        try:
            # 插入数据
            insert_foods_data(connection, data)
        finally:
            connection.close()
            logger.info("Database connection closed for foods")

    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_path}")
        raise
    except json.JSONDecodeError as err:
        logger.error(f"Invalid JSON format in {json_path}: {err}")
        raise
    except Exception as err:
        logger.error(f"Error processing foods.json: {err}")
        raise
            

def main():
    base_path = Path("C:/projects/ESOCN")
    #此处没有news
    json_files = {
        'equipment': base_path / "src/Data/equipment.json",
        'skills': base_path / "src/Data/skills.json",
        'furniture': base_path / "src/Data/furniture.json",
        'cpSkills': base_path / "src/Data/cpSkills.json",
        'buffs': base_path / "src/Data/buffs.json",
        'foods': base_path / "src/Data/foods.json",
        'collectibleFurniture': base_path / "src/Data/collectibleFurniture.json"
    }
    logger.info("Starting JSON to DATABASE import process")
    for category, json_path in json_files.items():
        if category == 'equipment':
            process_equipment_json(json_path)
        elif category == 'skills':
            process_skills_json(json_path)
        elif category == 'furniture':
            process_furniture_json(json_path)
        elif category == 'cpSkills':
            process_cpSkills_json(json_path)
        elif category == 'buffs':
            process_buffs_json(json_path)
        elif category == 'foods':
            process_foods_json(json_path)
        elif category == 'collectibles':
            process_collectibleFurniture_json(json_path)
    logger.info("Import process completed")

if __name__ == "__main__":
    main()