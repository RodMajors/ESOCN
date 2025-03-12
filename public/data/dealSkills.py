import json
import luadata
import asyncio
import aiomysql
import pdb

# 数据库连接信息
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lzr@136595755",
    "db": "esodata",
    "port": 3306,
    "charset": "utf8mb4"
}

# 异步数据库连接函数
async def connect_db():
    try:
        conn = await aiomysql.connect(**DB_CONFIG)
        return conn
    except aiomysql.Error as e:
        print(f"数据库连接失败: {e}")
        raise

# 异步查询函数
async def query_en_text(conn, en_text):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT enText FROM esotext WHERE zhText = %s LIMIT 1", (en_text,))
            result = await cursor.fetchone()
            return result[0] if result else None
    except aiomysql.Error as e:
        print(f"查询失败: {e}")
        return None

# 加载LUA文件
def load_lua_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lua_code = file.read()
    return luadata.unserialize(lua_code)

# 移除数字键，转换为数组
def convert_to_array(data):
    if isinstance(data, dict):
        # 分离数字键和非数字键
        digit_items = []
        non_digit_items = {}
        
        for k, v in data.items():
            if str(k).isdigit():
                digit_items.append((int(k), v))
            else:
                non_digit_items[k] = convert_to_array(v)
        
        # 对数字键的部分转换为数组
        digit_items.sort(key=lambda x: x[0])  # 按数字键排序
        digit_array = [convert_to_array(v) for k, v in digit_items]
        
        # 合并数组和非数字键的部分
        if non_digit_items:
            # 如果有非数字键，返回一个字典，包含数组和其他键值对
            return {"data": digit_array, **non_digit_items}
        else:
            # 如果只有数字键，返回数组
            return digit_array
    elif isinstance(data, list):
        # 如果是列表，递归处理每个元素
        return [convert_to_array(item) for item in data]
    else:
        return data

def convert_power_types(data):
    if isinstance(data, dict):
        # 检查是否是 powerTypes 标签
        if "powerTypes" in data:
            new_power_types = {}
            power_types = data["powerTypes"]
            if isinstance(power_types, list) and len(power_types) != 0:
                try:
                    new_power_types["magickaCost"] = power_types[0] ;
                except UnboundLocalError:
                    print(power_types[0])
            if isinstance(power_types, dict):
                # 创建一个新的字典来存储转换后的 powerTypes
                # 转换 [1], [4], [32] 为对应的键
                new_power_types["magickaCost"] = power_types.get(1, "")
                print("已经处理magickaCost")
                new_power_types["staminaCost"] = power_types.get(4, "")
                print("已经处理staminaCost")
                new_power_types["healthCost"] = power_types.get(32, "")
                print("已经处理healthCost")
                # 替换原来的 powerTypes
            data["powerTypes"] = new_power_types
        # 递归处理其他部分
        for k, v in data.items():
            data[k] = convert_power_types(v)
    elif isinstance(data, list):
        # 如果是列表，递归处理每个元素
        data = [convert_power_types(item) for item in data]
    return data

# 修改后的 convert_to_array 函数
def convert_to_array_with_power_types(data):
    data = convert_power_types(data)
    print(data)
    data = convert_to_array(data)
    return data

# 异步提取并合并数据
async def extract_and_merge_data(conn, cn_data, en_data):
    # 移除数字键并转换为数组
    cn_data_skills = convert_to_array_with_power_types(cn_data["Default"]["@Ha_Ren"]["$AccountWide"]["dataSkills"])
    en_data_skills = convert_to_array_with_power_types(en_data["Default"]["@Ha_Ren"]["$AccountWide"]["dataSkills"])

    # 合并数据
    for i, cn_type in enumerate(cn_data_skills):
        en_type = en_data_skills[i] if i < len(en_data_skills) else {}
        # 添加 enName 字段
        cn_type['enName'] = en_type.get('name', '')
        # 递归处理 skills
        if (cn_type['data']):
            for j, cn_class in enumerate(cn_type['data']): #神族之矛
                cn_class['enName'] = await query_en_text(conn, cn_class['name'])
                print(cn_class['name'], '翻译为', cn_class['enName'])
                if cn_class['skills']:
                    for k, cn_skills in enumerate(cn_class['skills']): #中心横扫
                        try:
                            cn_skills['enName'] = await query_en_text(conn, cn_skills['name'])
                            print(cn_skills['name'], '翻译为', cn_skills['enName'])
                            if cn_skills['data']:
                                for v, cn_skill in enumerate(cn_skills['data']):
                                    try:
                                        cn_skill['enName'] = await query_en_text(conn, cn_skill['name'])
                                        print(cn_skill['name'], '翻译为', cn_skill['enName'])
                                    except IndexError:
                                        print('en_skill IndexError: list index out of range\n')
                        except IndexError:
                            print('en_class IndexError list index out of range\n')

    return cn_data_skills

# 保存为JSON文件
def save_as_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 异步主函数
async def main():
    # 建立数据库连接
    conn = await connect_db()
    
    cn_lua_file = 'E:/projects/ESOCN/public/data/DataExtractor-Skills-cn.lua'
    en_lua_file = 'E:/projects/ESOCN/public/data/DataExtractor-Skills-en.lua'

    # 加载LUA文件
    cn_data = load_lua_file(cn_lua_file)
    en_data = load_lua_file(en_lua_file)

    # 提取并合并数据
    merged_data = await extract_and_merge_data(conn, cn_data, en_data)

    # 保存为JSON文件
    save_as_json(merged_data, 'merged_data.json')

    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())