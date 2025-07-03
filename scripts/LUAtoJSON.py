import json
import os
from pathlib import Path
import re
import luadata
from uuid import uuid4

def clean_name(name):
    """去除名称中的括号部分"""
    return re.sub(r'\s*\([^)]+\)', '', name).strip()

def extract_table(data, lang):
    """从 LUA 表中提取数据，处理字符串、数字、嵌套表和列表"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            key_str = str(key)
            if key_str == "icon" and isinstance(value, str) and value.endswith((".dds", ".webp")):
                value = value.replace(".dds", ".webp")
            result[key_str] = extract_table(value, lang)
        return result
    elif isinstance(data, list):
        return [extract_table(item, lang) for item in data]
    elif isinstance(data, (str, int, float, bool)):
        return str(data) if isinstance(data, (int, float)) else data
    else:
        print(f"Warning: Unexpected data type in extract_table: {type(data)}, value: {data}")
        return data

def extract_skill(skill_data, lang):
    """提取技能数据，处理 icon 和 powerTypes"""
    if not isinstance(skill_data, dict):
        print(f"Warning: skill_data is not a dict, type: {type(skill_data)}, value: {skill_data}")
        return {}
    
    power_types = skill_data.get("powerTypes", {})
    power_types_array = []
    
    # 处理 powerTypes 为字典的情况
    if isinstance(power_types, dict):
        print(f"Processing skill '{skill_data.get('name')}' powerTypes as dict: {power_types}")
        keys = {1: "magickaCost", 4: "staminaCost", 32: "healthCost"}
        power_type_entry = {
            "magickaCost": 0,
            "staminaCost": 0,
            "healthCost": 0
        }
        for key, name in keys.items():
            value = power_types.get(key)
            print(f"Key {key} ({name}): {value}")
            if value:
                power_type_entry[name] = value
        if any(power_type_entry.values()):
            power_types_array.append(power_type_entry)
    
    # 处理 powerTypes 为列表的情况（luadata 转换导致）
    elif isinstance(power_types, list) and power_types:
        print(f"Processing skill '{skill_data.get('name')}' powerTypes as list: {power_types}")
        # 假设列表第一个元素对应 magickaCost（键 1）
        power_type_entry = {
            "magickaCost": power_types[0] if power_types else 0,
            "staminaCost": 0,
            "healthCost": 0
        }
        power_types_array.append(power_type_entry)
    
    # 如果 powerTypes 为空或无效，添加默认值
    if not power_types_array:
        print(f"Warning: No valid powerTypes for skill '{skill_data.get('name')}', using default")
        power_types_array.append({"magickaCost": 0, "staminaCost": 0, "healthCost": 0})
    
    skill = {
        "id": str(skill_data.get("id", "")),
        "name": skill_data.get("name", "") if lang == "cn" else "",
        "enName": skill_data.get("name", "") if lang == "en" else "",
        "description": skill_data.get("description", ""),
        "icon": skill_data.get("icon", "").replace(".dds", ".webp"),
        "cost": skill_data.get("cost", 0),
        "powerTypes": power_types_array,
        "castTime": skill_data.get("castTime", 0),
        "target": skill_data.get("target", ""),
        "minRange": skill_data.get("minRange", 0),
        "maxRange": skill_data.get("maxRange", 0),
        "radius": skill_data.get("radius", 0),
        "duration": skill_data.get("duration", 0),
        "earnedRank": skill_data.get("earnedRank", 0),
        "isChanneled": skill_data.get("isChanneled", False),
        "isDamage": skill_data.get("isDamage", False),
        "isHealer": skill_data.get("isHealer", False),
        "isTank": skill_data.get("isTank", False),
        "passive": skill_data.get("passive", False),
        "ultimate": skill_data.get("ultimate", False)
    }
    
    if "parentAbilityId" in skill_data:
        skill["parentAbilityId"] = str(skill_data["parentAbilityId"])
    if "newEffect" in skill_data:
        skill["newEffect"] = skill_data["newEffect"]
    
    return skill

def get_icon_path(set_data):
    """提取套装的 icon 路径，优先从护甲.头部获取"""
    default_icon = ""
    icon_path = ""
    styles = set_data.get("styles", {})
    if "护甲" in styles and "头部" in styles["护甲"]:
        head_type = list(styles["护甲"].get("头部", {}).values())[0]
        icon_path = head_type.get("icon", "") if head_type else ""
    else:
        def get_first_icon(obj):
            if not obj:
                return ""
            if isinstance(obj, dict) and "icon" in obj:
                return obj["icon"]
            for value in obj.values():
                if isinstance(value, dict):
                    result = get_first_icon(value)
                    if result:
                        return result
            return ""
        icon_path = get_first_icon(styles)
    
    clean_path = icon_path.replace("/esoui/", "") if icon_path else ""
    return f"/esoui/{clean_path}" if clean_path else default_icon

def get_style(set_data):
    """提取套装的 style，优先从护甲.头部获取"""
    default_style = ""
    styles = set_data.get("styles", {})
    if "护甲" in styles and "头部" in styles["护甲"]:
        head_type = list(styles["护甲"].get("头部", {}).values())[0]
        return head_type.get("style", "") if head_type else ""
    else:
        def get_first_style(obj):
            if not obj:
                return ""
            if isinstance(obj, dict) and "style" in obj:
                return obj["style"]
            for value in obj.values():
                if isinstance(value, dict):
                    result = get_first_style(value)
                    if result:
                        return result
            return ""
        return get_first_style(styles)

def get_armor(set_data):
    """根据 type 和 styles 计算 armor 属性"""
    styles = set_data.get("styles", {})
    set_type = set_data.get("type")
    
    if set_type == 3:
        return "自选护甲类型"
    elif set_type == 12 and styles:
        first_style_key = next(iter(styles), None)
        if not first_style_key:
            return None
        first_sub_key = next(iter(styles.get(first_style_key), {}), None)
        if not first_sub_key:
            return None
        return "项链" if first_sub_key == "颈部装备" else first_sub_key
    else:
        if "护甲" not in styles and "武器" in styles:
            return "武器"
        armor_styles = styles.get("护甲", {})
        part_map = {
            "重型": "重甲",
            "中型": "中甲",
            "轻型": "轻甲"
        }
        types_set = set()
        for part in armor_styles.values():
            part_types = part.keys()
            for part_type in part_types:
                if part_type in part_map:
                    types_set.add(part_map[part_type])
        
        types_array = list(types_set)
        if not types_array:
            return None
        elif len(types_array) == 1:
            return types_array[0]
        elif len(types_array) == 3 and all(t in types_array for t in ["重甲", "中甲", "轻甲"]):
            return "随机护甲类型"
        return "随机护甲类型"

def find_data_path(data, target_key, path=None):
    """递归搜索数据中的目标键，返回其路径"""
    if path is None:
        path = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return path + [key]
            sub_path = find_data_path(value, target_key, path + [key])
            if sub_path:
                return sub_path
    elif isinstance(data, list):
        for i, item in enumerate(data):
            sub_path = find_data_path(item, target_key, path + [i])
            if sub_path:
                return sub_path
    return None

def get_user_account(data, category, is_special=False):
    """动态获取包含指定类别的用户账户名"""
    default_data = data.get("Default", {})
    if not isinstance(default_data, dict):
        print(f"Error: Default is not a dict, type: {type(default_data)}")
        return None
    
    for account_name, account_data in default_data.items():
        if not account_name.startswith("@"):
            continue
        if is_special:
            account_path = account_data.get("$AccountWide", {}).get(category)
        else:
            account_path = account_data.get("$AccountWide", {}).get("dataItems", {}).get(category)
        if account_path:
            print(f"Found account for {category}: {account_name}")
            return account_name
    print(f"No account found for {category}")
    return None

def process_sets(cn_data, en_data):
    """处理 Sets 类别，提取并合并中英文数据"""
    equipment = []
    
    cn_account = get_user_account(cn_data, "Sets")
    en_account = get_user_account(en_data, "Sets")
    if not cn_account or not en_account:
        print(f"CN or EN account not found for Sets (CN: {cn_account}, EN: {en_account})")
        return equipment
    
    cn_path = ["Default", cn_account, "$AccountWide", "dataItems", "Sets"]
    cn_sets = cn_data
    for key in cn_path:
        cn_sets = cn_sets.get(key, {})
        if not cn_sets:
            print(f"CN - Key '{key}' not found in Sets path: {cn_path}")
            return equipment
    
    en_path = ["Default", en_account, "$AccountWide", "dataItems", "Sets"]
    en_sets = en_data
    for key in en_path:
        en_sets = en_sets.get(key, {})
        if not en_sets:
            print(f"EN - Key '{key}' not found in Sets path: {en_path}")
            return equipment
    
    if not isinstance(cn_sets, dict):
        print(f"Error: cn_sets is not a dict, type: {type(cn_sets)}, value: {cn_sets}")
        return equipment
    
    # 处理中文 Sets
    cn_equipment = []
    for key, set_data in cn_sets.items():
        set_data = extract_table(set_data, "cn")
        print(f"Processing CN set: key={key}, name={set_data.get('name', '')}, bonuses={bool(set_data.get('bonuses'))}, styles={bool(set_data.get('styles'))}")
        set_entry = {
            "key": str(key),
            "name": set_data.get("name", ""),
            "place": set_data.get("place", ""),
            "bonuses": {
                f"effect{i}": set_data.get("bonuses", {}).get(str(i), "") for i in range(2, 14)
            },
            "id": str(set_data.get("id", "")),
            "type": str(set_data.get("type", "")),
            "styles": set_data.get("styles", {})
        }
        cn_equipment.append(set_entry)
    
    # 处理英文 Sets
    en_equipment = []
    if not isinstance(en_sets, dict):
        print(f"Error: en_sets is not a dict, type: {type}, value: {en_sets}")
    else:
        for key, set_data in en_sets.items():
            set_data = extract_table(set_data, "en")
            print(f"Processing EN set: key={key}, name={set_data.get('name', '')}")
            set_entry = {
                "key": str(key),
                "enName": set_data.get("name", ""),
                "enplace": set_data.get("place", "")
            }
            en_equipment.append(set_entry)
    
    # 合并中英文数据
    for cn_set in cn_equipment:
        en_set = next((e for e in en_equipment if e["key"] == cn_set["key"]), None)
        if en_set and en_set["enName"]:
            print(f"Merging set: key={cn_set['key']}, CN name={cn_set['name']}, EN name={en_set['enName']}")
            merged_set = {
                "name": cn_set["name"],
                "enName": en_set["enName"],
                "place": cn_set["place"],
                "enplace": en_set["enplace"],
                "bonuses": cn_set["bonuses"],
                "id": cn_set["id"],
                "type": cn_set["type"],
                "styles": cn_set["styles"]
            }
        else:
            print(f"No English match found for set with key: {cn_set['key']}")
            merged_set = {
                **cn_set,
                "enName": cn_set["name"],
                "enplace": cn_set["place"]
            }
        equipment.append(merged_set)
    
    print(f"Processed {len(equipment)} Sets before post-processing")
    equipment = post_process_sets(equipment)
    print(f"Processed {len(equipment)} Sets after post-processing")
    return equipment

def post_process_sets(equipment):
    """对合并后的 Sets 数据进行后处理"""
    set_map = {set_data["enName"]: set_data for set_data in equipment}
    
    # 过滤 place 为空的套装
    filtered_equipment = []
    for set_data in equipment:
        if set_data["place"] == "":
            if set_data["type"] == "2":
                set_data["place"] = "竞技场"
                set_data["enplace"] = "Battlefield"
                filtered_equipment.append(set_data)
        else:
            filtered_equipment.append(set_data)
    
    # 处理 Perfected 套装逻辑并添加 icon, style, armor
    for set_data in filtered_equipment:
        if set_data["enName"].startswith("Perfected "):
            base_name = set_data["enName"].replace("Perfected ", "")
            base_set = set_map.get(base_name)
            if base_set and base_set["bonuses"].get("effect5"):
                set_data["bonuses"]["effect6"] = base_set["bonuses"]["effect5"]
                print(f"Applied Perfected logic for {set_data['enName']}: copied effect5 from {base_name}")
        
        set_data["icon"] = get_icon_path(set_data)
        set_data["style"] = get_style(set_data)
        set_data["armor"] = get_armor(set_data)
    
    return filtered_equipment[::-1]  # 反转顺序

def process_foods(cn_data, en_data):
    """处理 Foods 类别，提取并合并中英文数据"""
    foods = []
    
    cn_account = get_user_account(cn_data, "Foods")
    en_account = get_user_account(en_data, "Foods")
    if not cn_account or not en_account:
        print(f"CN or EN account not found for Foods (CN: {cn_account}, EN: {en_account})")
        return foods
    
    cn_path = ["Default", cn_account, "$AccountWide", "dataItems", "Foods"]
    cn_foods = cn_data
    for key in cn_path:
        cn_foods = cn_foods.get(key, {})
        if not cn_foods:
            print(f"CN - Key '{key}' not found in Foods path: {cn_path}")
            return foods
    
    en_path = ["Default", en_account, "$AccountWide", "dataItems", "Foods"]
    en_foods = en_data
    for key in en_path:
        en_foods = en_foods.get(key, {})
        if not en_foods:
            print(f"EN - Key '{key}' not found in Foods path: {en_path}")
            return foods
    
    if not isinstance(cn_foods, dict):
        print(f"Error: cn_foods is not a dict, type: {type(cn_foods)}, value: {cn_foods}")
        return foods
    
    # 处理中文 Foods
    for key, food_data in cn_foods.items():
        food_data = extract_table(food_data, "cn")
        print(f"Processing CN food: key={key}, name={food_data.get('name', '')}, description={bool(food_data.get('description'))}, ingredients={bool(food_data.get('ingredients'))}")
        food_entry = {
            "name": food_data.get("name", ""),
            "enName": "",
            "ingredients": food_data.get("ingredients", ""),
            "id": str(food_data.get("id", "")),
            "icon": food_data.get("icon", "").replace(".dds", ".webp"),
            "itemTypeText": food_data.get("itemTypeText", ""),
            "quality": food_data.get("quality", ""),
            "description": food_data.get("description", ""),
            "canBeCrafted": food_data.get("canBeCrafted", False),
            "specializedItemTypeText": food_data.get("specializedItemTypeText", "")
        }
        
        # 处理英文 Foods
        if not isinstance(en_foods, dict):
            print(f"Error: en_foods is not a dict, type: {type(en_foods)}, value: {en_foods}")
        else:
            en_food = en_foods.get(key, {})
            if en_food:
                en_food = extract_table(en_food, "en")
                food_entry["enName"] = en_food.get("name", food_entry["name"])
                print(f"Found EN food: key={key}, enName={food_entry['enName']}")
            else:
                print(f"No English match found for food with key: {key}")
        
        foods.append(food_entry)
    
    print(f"Processed {len(foods)} Foods")
    return foods

def process_collectible_furniture(cn_data, en_data):
    """处理 CollectibleFurniture 类别，提取并合并中英文数据"""
    furniture = []
    
    cn_account = get_user_account(cn_data, "CollectibleFurniture")
    en_account = get_user_account(en_data, "CollectibleFurniture")
    if not cn_account or not en_account:
        print(f"中文或英文账户未找到 (中文: {cn_account}, 英文: {en_account})")
        return furniture
    
    cn_path = ["Default", cn_account, "$AccountWide", "dataItems", "CollectibleFurniture"]
    cn_furniture = cn_data
    for key in cn_path:
        cn_furniture = cn_furniture.get(key, {})
        if not cn_furniture:
            print(f"中文 - 路径 {cn_path} 中未找到键 '{key}'")
            return furniture
    
    en_path = ["Default", en_account, "$AccountWide", "dataItems", "CollectibleFurniture"]
    en_furniture = en_data
    for key in en_path:
        en_furniture = en_furniture.get(key, {})
        if not en_furniture:
            print(f"英文 - 路径 {en_path} 中未找到键 '{key}'")
            return furniture
    
    if not isinstance(cn_furniture, dict):
        print(f"错误: cn_furniture 不是字典，类型: {type(cn_furniture)}, 值: {cn_furniture}")
        return furniture
    
    for key, furn_data in cn_furniture.items():
        furn_data = extract_table(furn_data, "cn")
        print(f"处理中文收藏家具: id={furn_data.get('id', '')}, 名称={furn_data.get('name', '')}, 描述={bool(furn_data.get('description'))}")
        furn_entry = {
            "name": furn_data.get("name", ""),
            "enName": "",
            "id": str(furn_data.get("id", "")),
            "icon": furn_data.get("icon", "").replace(".dds", ".webp"),
            "category": furn_data.get("category", ""),  # 使用 category 作为 itemTypeText
            "description": furn_data.get("description", ""),
            "canBeCrafted": furn_data.get("canBeCrafted", False),
            "hint": furn_data.get("hint", ""),  # 使用 hint 作为 specializedItemTypeText
            "furnitureId": str(furn_data.get("furnitureId", ""))  # 新增 furnitureId 字段
        }
        
        if not isinstance(en_furniture, dict):
            print(f"错误: en_furniture 不是字典，类型: {type(en_furniture)}, 值: {en_furniture}")
        else:
            en_furn = en_furniture.get(key, {})
            if en_furn:
                en_furn = extract_table(en_furn, "en")
                furn_entry["enName"] = en_furn.get("name", furn_entry["name"])
                print(f"找到英文收藏家具: id={furn_entry['id']}, 英文名称={furn_entry['enName']}")
            else:
                print(f"未找到 id 为 {furn_entry['id']} 的英文收藏家具")
        
        furniture.append(furn_entry)
    
    print(f"处理了 {len(furniture)} 个收藏家具")
    return furniture

def process_furniture(cn_data, en_data):
    """处理 Furniture 类别，提取并合并中英文数据"""
    furniture = []
    
    cn_account = get_user_account(cn_data, "Furniture")
    en_account = get_user_account(en_data, "Furniture")
    if not cn_account or not en_account:
        print(f"CN or EN account not found for Furniture (CN: {cn_account}, EN: {en_account})")
        return furniture
    
    cn_path = ["Default", cn_account, "$AccountWide", "dataItems", "Furniture"]
    cn_furniture = cn_data
    for key in cn_path:
        cn_furniture = cn_furniture.get(key, {})
        if not cn_furniture:
            print(f"CN - Key '{key}' not found in Furniture path: {cn_path}")
            return furniture
    
    en_path = ["Default", en_account, "$AccountWide", "dataItems", "Furniture"]
    en_furniture = en_data
    for key in en_path:
        en_furniture = en_furniture.get(key, {})
        if not en_furniture:
            print(f"ENF - Key '{key}' not found in Furniture path::en_path: {en_path}")
            return furniture
    
    if not isinstance(cn_furniture, dict):
        print(f"Error: cn_furniture is not a dict, type: {type(cn_furniture)}, value: {en_furniture}")
        return furniture
    
    for key, furn_data in cn_furniture.items():
        furn_data = extract_table(furn_data, "cn")
        print(f"Processing CN furniture: id={furn_data.get('id', '')}, name={furn_data.get('name', '')}, description={bool(furn_data.get('description'))}")
        furn_entry = {
            "name": furn_data.get("name", ""),
            "enName": "",
            "ingredients": furn_data.get("ingredients", ""),
            "id": str(furn_data.get("id", "")),
            "icon": furn_data.get("icon", "").replace(".dds", ".webp"),
            "type": furn_data.get("itemTypeText", ""),
            "quality": furn_data.get("quality", ""),
            "description": furn_data.get("description", ""),
            "canBeCrafted": False,
            "category": furn_data.get("category", ""),
            "subCategory": furn_data.get("subcategory", ""),
            "skills": ""
        }
        
        if not isinstance(en_furniture, dict):
            print(f"Error: en_furniture is not a dict, type: {type(en_furniture)}, value: {en_furniture}")
        else:
            en_furn = en_furniture.get(key, {})
            if en_furn:
                en_furn = extract_table(en_furn, "en")
                furn_entry["enName"] = en_furn.get("name", furn_entry["name"])
                print(f"Found EN furniture: id={furn_entry['id']}, enName={furn_entry['enName']}")
            else:
                print(f"No English match found for furniture with id: {furn_entry['id']}")
        
        furniture.append(furn_entry)
    
    print(f"Processed {len(furniture)} Furniture")
    return furniture

def process_cp_skills(cn_data, en_data, export_json):
    """处理 dataCpSkills 类别，合并中英文数据和 exportJson 数据"""
    skills = []
    
    cn_account = get_user_account(cn_data, "dataCpSkills", is_special=True)
    en_account = get_user_account(en_data, "dataCpSkills", is_special=True)
    if not cn_account or not en_account:
        print(f"CN or EN account not found for dataCpSkills (CN: {cn_account}, EN: {en_account})")
        return skills
    
    cn_path = ["Default", cn_account, "$AccountWide", "dataCpSkills"]
    cn_skills = cn_data
    for key in cn_path:
        cn_skills = cn_skills.get(key, {})
        if not cn_skills:
            print(f"CN - Key '{key}' not found in dataCpSkills path: {cn_path}")
            return skills
    
    en_path = ["Default", en_account, "$AccountWide", "dataCpSkills"]
    en_skills = en_data
    for key in en_path:
        en_skills = en_skills.get(key, {})
        if not cn_skills:
            print(f"EN - Key '{key}' not found in dataCpSkills path: {en_path}")
            return skills
    
    # 处理中文 dataCpSkills
    cn_skills_list = []
    if not isinstance(cn_skills, list):
        print(f"Error: cn_skills is not a list, type: {type(cn_skills)}, value: {cn_skills}")
        return skills
    for category_idx, category_data in enumerate(cn_skills, 1):
        if not isinstance(category_data, dict):
            print(f"Warning: category_data at index {category_idx} is not a dict, type: {type(category_data)}")
            continue
        category_id = str(category_data.get("id", category_idx))
        skills_data = category_data.get("skills", [])
        if not isinstance(skills_data, list):
            print(f"Warning: skills_data for category {category_id} is not a list, type: {type(skills_data)}")
            continue
        for skill_idx, skill_data in enumerate(skills_data, 1):
            skill_data = extract_table(skill_data, "cn")
            skill_entry = {
                "categoryId": category_id,
                "skillId": str(skill_data.get("id", skill_idx)),
                "name": clean_name(skill_data.get("name", "")),
                "id": str(skill_data.get("id", "")),
                "description": skill_data.get("description", ""),
                "isSlottable": skill_data.get("isSlottable", False),
                "clusterName": skill_data.get("clusterName", ""),
                "index": str(skill_data.get("index", skill_idx)),
                "bounsText": skill_data.get("bounsText", {}),
                "isInCluster": skill_data.get("isInCluster", False),
                "type": skill_data.get("type", 0)
            }
            cn_skills_list.append(skill_entry)
    
    print(f"Processed {len(cn_skills_list)} CN CpSkills")
    
    # 处理英文 dataCpSkills
    en_skills_list = []
    if not isinstance(en_skills, list):
        print(f"Error: en_skills is not a list, type: {type(en_skills)}, value: {cn_skills}")
        return skills
    for category_idx, category_data in enumerate(en_skills, 1):
        if not isinstance(category_data, dict):
            print(f"Warning: category_data at index {category_idx} is not a dict, type: {type(category_data)}")
            continue
        category_id = str(category_data.get("id", category_idx))
        skills_data = category_data.get("skills", [])
        if not isinstance(skills_data, list):
            print(f"Warning: skills_data for category {category_id} is not a list, type: {type(skills_data)}")
            continue
        for skill_idx, skill_data in enumerate(skills_data, 1):
            skill_data = extract_table(skill_data, "en")
            skill_entry = {
                "categoryId": category_id,
                "skillId": str(skill_data.get("id", skill_idx)),
                "id": str(skill_data.get("id", "")),
                "enName": skill_data.get("name", "")
            }
            en_skills_list.append(skill_entry)
    
    print(f"Processed {len(en_skills_list)} EN CpSkills")
    
    # 加载 exportJson 数据
    export_skills = export_json.get("cp2Skills", [])
    if not isinstance(export_skills, list):
        print(f"Error: cp2Skills is not a list, type: {type(export_skills)}, value: {export_skills}")
        return skills
    export_lookup = {str(skill.get("skillId", "")): skill for skill in export_skills if "skillId" in skill}
    
    # 合并数据
    for cn_skill in cn_skills_list:
        skill_id = cn_skill["id"]
        category_id = cn_skill["categoryId"]
        en_skill = next((e for e in en_skills_list if str(e["id"]) == skill_id and e["categoryId"] == category_id), None)
        export_skill = export_lookup.get(skill_id, {})
        
        merged_skill = {
            "name": cn_skill["name"],
            "enName": export_skill.get("name", en_skill["enName"] if en_skill else cn_skill["name"]),
            "description": cn_skill["description"],
            "isSlottable": cn_skill["isSlottable"],
            "clusterName": cn_skill["clusterName"],
            "index": cn_skill["index"],
            "bounsText": cn_skill["bounsText"],
            "isInCluster": cn_skill["isInCluster"],
            "id": skill_id,
            "type": cn_skill["type"],
            "categoryId": category_id,
            "maxPoints": export_skill.get("maxPoints", ""),
            "jumpPoints": export_skill.get("jumpPoints", ""),
            "numJumpPoints": export_skill.get("numJumpPoints", ""),
            "jumpPointDelta": export_skill.get("jumpPointDelta", "")
        }
        skills.append(merged_skill)
    
    print(f"Merged {len(skills)} CpSkills")
    return skills

def post_process_skills(skills):
    """对 skills 数据进行后处理，修改 typeName 和删除特定 categoryName"""
    # 定义 typeName 修改映射
    type_name_map = {
        "黑暗魔法": "巫师",
        "魔族召唤": "巫师",
        "风暴呼唤": "巫师",
        "神族之矛": "圣殿骑士",
        "黎明之怒": "圣殿骑士",
        "恢复之光": "圣殿骑士",
        "烈焰之刃": "龙骑士",
        "巨龙之力": "龙骑士",
        "大地之心": "龙骑士",
        "刺杀": "夜刃",
        "暗影": "夜刃",
        "虹吸": "夜刃",
        "动物伙伴": "守望者",
        "绿色平衡": "守望者",
        "凛冬之拥": "守望者",
        "墓穴领主": "死灵法师",
        "白骨暴君": "死灵法师",
        "存世亡者": "死灵法师",
        "古籍使者": "奥术师",
        "异典士兵": "奥术师",
        "药剂符师": "奥术师"
    }
    
    # 定义 typeEnName 映射
    type_en_name_map = {
        "奥术师": "Arcanist",
        "圣殿骑士": "Templar",
        "龙骑士": "DragonKnight",
        "夜刃": "NightBlade",
        "巫师": "Sorcerer",
        "守望者": "Warden",
        "死灵法师": "Necromancer",
        "武器": "Weapon",
        "护甲": "Armor",
        "世界": "World",
        "公会": "Guild",
        "联盟战争": "Alliance War",
        "种族": "Racial",
        "制作": "Craft"
    }
    
    # 定义需要删除的 categoryName
    delete_categories = {
        "Cyrodiil Champion DPS",
        "Cyrodiil Champion Tank",
        "西罗帝尔勇士支援",
        "复仇烈焰之刃",
        "复仇巨龙之力",
        "复仇大地之心",
        "复仇刺杀",
        "复仇暗影",
        "复仇虹吸",
        "复仇神族之矛",
        "复仇黎明之怒",
        "复仇恢复之光",
        "复仇魔族的召唤",
        "复仇黑暗魔法",
        "复仇风暴呼唤",
        "复仇动物伙伴",
        "复仇绿色平衡",
        "复仇凛冬之拥",
        "复仇墓穴领主",
        "复仇白骨暴君",
        "复仇存世亡者",
        "复仇药剂符师",
        "复仇异典士兵",
        "复仇古籍使者"
    }
    
    filtered_skills = []
    for skill in skills:
        category_name = skill.get("categoryName", "")
        
        # 检查是否需要删除
        if category_name in delete_categories:
            continue
        
        # 更新 typeName 和 typeEnName
        if category_name in type_name_map:
            old_type_name = skill["typeName"]
            skill["typeName"] = type_name_map[category_name]
            skill["typeEnName"] = type_en_name_map.get(skill["typeName"], skill["typeEnName"])
            
            # 更新 advance 中的 typeName 和 typeEnName
            for advance in skill.get("advance", []):
                advance["typeName"] = skill["typeName"]
                advance["typeEnName"] = skill["typeEnName"]
                advance["categoryName"] = skill["categoryName"]
                advance["categoryEnName"] = skill["categoryEnName"]
        
        filtered_skills.append(skill)
    
    print(f"Post-processed skills: {len(skills)} -> {len(filtered_skills)} skills after filtering")
    return filtered_skills

def process_skills(cn_data, en_data):
    """处理 dataSkills，合并中英文数据"""
    skills = []
    
    # 获取账户
    cn_account = get_user_account(cn_data, "dataSkills", is_special=True)
    en_account = get_user_account(en_data, "dataSkills", is_special=True)
    print(f"CN account for dataSkills: {cn_account}")
    print(f"EN account for dataSkills: {en_account}")
    if not cn_account or not en_account:
        print(f"CN or EN account not found for dataSkills (CN: {cn_account}, EN: {en_account})")
        return skills
    
    # 提取中文 dataSkills
    cn_path = ["Default", cn_account, "$AccountWide", "dataSkills"]
    cn_skills = cn_data
    for key in cn_path:
        cn_skills = cn_skills.get(key, {})
        print(f"CN - Accessing key '{key}' in path: {cn_path}, current value type: {type(cn_skills)}")
        if not cn_skills:
            print(f"CN - Key '{key}' not found or empty in dataSkills path")
            return skills
    
    # 提取英文 dataSkills
    en_path = ["Default", en_account, "$AccountWide", "dataSkills"]
    en_skills = en_data
    for key in en_path:
        en_skills = en_skills.get(key, {})
        if not en_skills:
            print(f"EN - Key '{key}' not found or empty in dataSkills path")
            return skills
    
    # 处理中文 dataSkills
    cn_skills_list = []
    if not isinstance(cn_skills, list):
        print(f"Error: cn_skills is not a list, type: {type(cn_skills)}, value: {cn_skills}")
        return skills
    for type_idx, cn_type in enumerate(cn_skills, 1):
        if not isinstance(cn_type, dict):
            print(f"Warning: cn_type at index {type_idx} is not a dict, type: {type(cn_type)}")
            continue
        type_name = cn_type.get("name", f"Type {type_idx}")
        for key, category_data in cn_type.items():
            if key == "name" or not isinstance(key, int):
                continue
            if not isinstance(category_data, dict):
                print(f"Warning: category_data at type {type_idx}, key {key} is not a dict, type: {type(category_data)}")
                continue
            category_id = str(category_data.get("id", key))
            category_name = category_data.get("name", f"Category {key}")
            skills_data = category_data.get("skills", [])
            if not isinstance(skills_data, list):
                print(f"Warning: skills_data for category {category_id} is not a list, type: {type(skills_data)}")
                continue
            for skill_idx, skill_data in enumerate(skills_data, 1):
                if not isinstance(skill_data, dict):
                    print(f"Warning: skill_data at type {type_idx}, category {key}, skill {skill_idx} is not a dict, type: {type(skill_data)}")
                    continue
                skill_entry = extract_skill(skill_data, "cn")
                advance_skills = []
                for advance_idx in [1, 2]:
                    advance_data = skill_data.get(advance_idx, {})
                    if advance_data:
                        advance_entry = extract_skill(advance_data, "cn")
                        advance_skills.append(advance_entry)
                skill_entry["advance"] = advance_skills
                skill_entry["categoryId"] = category_id
                skill_entry["categoryName"] = category_name
                skill_entry["categoryEnName"] = ""  # 占位，稍后填充
                skill_entry["typeName"] = type_name
                skill_entry["typeEnName"] = ""  # 占位，稍后填充
                cn_skills_list.append(skill_entry)
    
    print(f"Processed {len(cn_skills_list)} CN Skills")
    
    # 处理英文 dataSkills
    en_skills_list = []
    if not isinstance(en_skills, list):
        print(f"Error: en_skills is not a list, type: {type(en_skills)}, value: {en_skills}")
        return skills
    for type_idx, en_type in enumerate(en_skills, 1):
        if not isinstance(en_type, dict):
            print(f"Warning: en_type at index {type_idx} is not a dict, type: {type(en_type)}")
            continue
        type_name = en_type.get("name", f"Type {type_idx}")
        for key, category_data in en_type.items():
            if key == "name" or not isinstance(key, int):
                continue
            if not isinstance(category_data, dict):
                print(f"Warning: category_data at type {type_idx}, key {key} is not a dict, type: {type(category_data)}")
                continue
            category_id = str(category_data.get("id", key))
            category_name = category_data.get("name", f"Category {key}")
            skills_data = category_data.get("skills", [])
            if not isinstance(skills_data, list):
                print(f"Warning: skills_data for category {category_id} is not a list, type: {type(skills_data)}")
                continue
            for skill_idx, skill_data in enumerate(skills_data, 1):
                if not isinstance(skill_data, dict):
                    print(f"Warning: skill_data at type {type_idx}, category {key}, skill {skill_idx} is not a dict, type: {type(skill_data)}")
                skill_entry = extract_skill(skill_data, "en")
                advance_skills = []
                for advance_idx in [1, 2]:
                    advance_data = skill_data.get(advance_idx, {})
                    if advance_data:
                        advance_entry = extract_skill(advance_data, "en")
                        advance_skills.append(advance_entry)
                skill_entry["advance"] = advance_skills
                skill_entry["categoryId"] = category_id
                skill_entry["categoryName"] = category_name
                skill_entry["categoryEnName"] = category_name
                skill_entry["typeName"] = type_name
                skill_entry["typeEnName"] = type_name
                en_skills_list.append(skill_entry)
    
    print(f"Processed {len(en_skills_list)} EN Skills")
    
    # 合并数据
    for cn_skill in cn_skills_list:
        skill_id = cn_skill["id"]
        en_skill = next((e for e in en_skills_list if e["id"] == skill_id and e["categoryId"] == cn_skill["categoryId"]), None)
        print(en_skill)
        merged_skill = {
            "name": cn_skill["name"],
            "enName": en_skill["enName"] if en_skill else cn_skill["name"],
            "description": cn_skill["description"],
            "icon": cn_skill["icon"],
            "id": skill_id,
            "cost": cn_skill["cost"],
            "powerTypes": cn_skill["powerTypes"],
            "castTime": cn_skill["castTime"],
            "target": cn_skill["target"],
            "minRange": cn_skill["minRange"],
            "maxRange": cn_skill["maxRange"],
            "radius": cn_skill["radius"],
            "duration": cn_skill["duration"],
            "earnedRank": cn_skill["earnedRank"],
            "isChanneled": cn_skill["isChanneled"],
            "isDamage": cn_skill["isDamage"],
            "isHealer": cn_skill["isHealer"],
            "isTank": cn_skill["isTank"],
            "passive": cn_skill["passive"],
            "ultimate": cn_skill["ultimate"],
            "advance": [],
            "categoryId": cn_skill["categoryId"],
            "categoryName": cn_skill["categoryName"],
            "categoryEnName": en_skill["categoryEnName"] if en_skill else cn_skill["categoryName"],
            "typeName": cn_skill["typeName"],
            "typeEnName": en_skill["typeEnName"] if en_skill else cn_skill["typeName"]
        }
        
        # 合并进阶技能
        for cn_advance in cn_skill["advance"]:
            advance_id = cn_advance["id"]
            en_advance = next((e for e in en_skill["advance"] if e["id"] == advance_id), None) if en_skill else None
            print(f"Merging advance skill ID {advance_id}, EN advance found: {bool(en_advance)}")
            merged_advance = {
                "name": cn_advance["name"],
                "enName": en_advance["enName"] if en_advance else cn_advance["name"],
                "description": cn_advance["description"],
                "icon": cn_advance["icon"],
                "id": advance_id,
                "cost": cn_advance["cost"],
                "powerTypes": cn_advance["powerTypes"],
                "castTime": cn_advance["castTime"],
                "target": cn_advance["target"],
                "minRange": cn_advance["minRange"],
                "maxRange": cn_advance["maxRange"],
                "radius": cn_advance["radius"],
                "duration": cn_advance["duration"],
                "earnedRank": cn_advance["earnedRank"],
                "isChanneled": cn_advance["isChanneled"],
                "isDamage": cn_advance["isDamage"],
                "isHealer": cn_advance["isHealer"],
                "isTank": cn_advance["isTank"],
                "passive": cn_skill["passive"],
                "ultimate": cn_advance["ultimate"],
                "parentAbilityId": cn_advance.get("parentAbilityId", ""),
                "newEffect": cn_advance.get("newEffect", ""),
                "categoryId": cn_skill["categoryId"],
                "categoryName": cn_skill["categoryName"],
                "categoryEnName": en_skill["categoryEnName"] if en_skill else cn_skill["categoryName"],
                "typeName": cn_skill["typeName"],
                "typeEnName": en_skill["typeEnName"] if en_skill else cn_skill["typeName"]
            }
            merged_skill["advance"].append(merged_advance)
        
        skills.append(merged_skill)
    
    print(f"Merged {len(skills)} Skills")
    
    # 后处理 skills
    skills = post_process_skills(skills)
    
    return skills

def process_recipes(cn_data, en_data):
    """处理 Recipes 类别，提取并合并中英文数据"""
    recipes = []
    
    # 获取账户
    cn_account = get_user_account(cn_data, "Recipes")
    en_account = get_user_account(en_data, "Recipes")
    if not cn_account or not en_account:
        print(f"中文或英文账户未找到 (中文: {cn_account}, 英文: {en_account})")
        return recipes
    
    # 提取中文 Recipes 数据
    cn_path = ["Default", cn_account, "$AccountWide", "dataItems", "Recipes"]
    cn_recipes = cn_data
    for key in cn_path:
        cn_recipes = cn_recipes.get(key, {})
        if not cn_recipes:
            print(f"中文 - 路径 {cn_path} 中未找到键 '{key}'")
            return recipes
    
    # 提取英文 Recipes 数据
    en_path = ["Default", en_account, "$AccountWide", "dataItems", "Recipes"]
    en_recipes = en_data
    for key in en_path:
        en_recipes = en_recipes.get(key, {})
        if not en_recipes:
            print(f"英文 - 路径 {en_path} 中未找到键 '{key}'")
            return recipes
    
    # 验证数据类型
    if not isinstance(cn_recipes, dict):
        print(f"错误: cn_recipes 不是字典，类型: {type(cn_recipes)}, 值: {cn_recipes}")
        return recipes
    
    # 处理中文 Recipes
    for key, recipe_data in cn_recipes.items():
        recipe_data = extract_table(recipe_data, "cn")
        print(f"处理中文配方: id={recipe_data.get('id', '')}, 名称={recipe_data.get('name', '')}, 材料={bool(recipe_data.get('ingredients'))}")
        recipe_entry = {
            "name": recipe_data.get("name", ""),
            "enName": "",  # 占位，稍后填充英文名称
            "ingredients": recipe_data.get("ingredients", ""),
            "id": str(recipe_data.get("id", "")),
            "quality": recipe_data.get("quality", ""),
            "type": recipe_data.get("type", ""),  # 使用 type 作为 type
            "skills": recipe_data.get("skills", "")  # 使用 skills 作为 specializedItemTypeText
        }
        
        # 处理英文 Recipes
        if not isinstance(en_recipes, dict):
            print(f"错误: en_recipes 不是字典，类型: {type(en_recipes)}, 值: {en_recipes}")
        else:
            en_recipe = en_recipes.get(key, {})
            if en_recipe:
                en_recipe = extract_table(en_recipe, "en")
                recipe_entry["enName"] = en_recipe.get("name", recipe_entry["name"])
                print(f"找到英文配方: id={recipe_entry['id']}, 英文名称={recipe_entry['enName']}")
            else:
                print(f"未找到 id 为 {recipe_entry['id']} 的英文配方")
        
        recipes.append(recipe_entry)
    
    print(f"处理了 {len(recipes)} 个配方")
    return recipes

def merge_food_ingredients():
    # 定义文件路径
    base_path = Path("C:/projects/ESOCN/src/Data")
    foods_file = base_path / "foods.json"
    recipes_file = base_path / "recipes.json"
    output_file = base_path / "foods.json"  # 输出新文件以避免覆盖原始文件

    # 读取 JSON 文件
    try:
        with open(foods_file, "r", encoding="utf-8") as f:
            foods_data = json.load(f)
        with open(recipes_file, "r", encoding="utf-8") as f:
            recipes_data = json.load(f)
    except Exception as e:
        print(f"读取 JSON 文件出错: {e}")
        return

    # 确保数据结构正确
    if not isinstance(foods_data.get("foods", []), list):
        print(f"错误: foods.json 的 'foods' 不是列表，类型: {type(foods_data.get('foods'))}")
        return
    if not isinstance(recipes_data.get("recipes", []), list):
        print(f"错误: recipes.json 的 'recipes' 不是列表，类型: {type(recipes_data.get('recipes'))}")
        return

    # 创建 foods 的名称到条目的映射
    foods_map = {item["name"]: item for item in foods_data["foods"]}

    # 统计更新计数
    updated_count = 0

    # 遍历 recipes，寻找以“配方：”开头的条目
    for recipe in recipes_data["recipes"]:
        recipe_name = recipe.get("name", "")
        if recipe_name.startswith("配方："):
            # 提取去掉前缀后的名称
            base_name = recipe_name[len("配方："):]
            food_item = foods_map.get(base_name)
            if food_item:
                food_item["canBeCrafted"] = "True" 
                # 检查 foods 中 ingredients 是否为空
                if not food_item.get("ingredients", "").strip():
                    # 复制 recipes 中的 ingredients
                    food_item["ingredients"] = recipe.get("ingredients", "")
                    updated_count += 1
                    print(f"更新配方: {base_name}, 新增材料: {food_item['ingredients']}")
                else:
                    print(f"跳过 {base_name}: ingredients 已存在 ({food_item['ingredients']})")
            else:
                print(f"未在 foods.json 中找到匹配的配方: {base_name}")

    # 保存更新后的 foods 数据
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(foods_data, f, ensure_ascii=False, indent=2)
        print(f"更新完成，修改了 {updated_count} 个配方的 ingredients，输出到 {output_file}")
    except Exception as e:
        print(f"写入 foods_updated.json 出错: {e}")

def merge_furniture_ingredients():
    # 定义文件路径
    base_path = Path("C:/projects/ESOCN/src/Data")
    furniture_file = base_path / "furniture.json"
    recipes_file = base_path / "recipes.json"
    output_file = base_path / "furniture.json"  # 直接覆盖 furniture.json

    # 读取 JSON 文件
    try:
        with open(furniture_file, "r", encoding="utf-8") as f:
            furniture_data = json.load(f)
        with open(recipes_file, "r", encoding="utf-8") as f:
            recipes_data = json.load(f)
    except Exception as e:
        print(f"读取 JSON 文件出错: {e}")
        return

    # 确保数据结构正确
    if not isinstance(furniture_data.get("furniture", []), list):
        print(f"错误: furniture.json 的 'furniture' 不是列表，类型: {type(furniture_data.get('furniture'))}")
        return
    if not isinstance(recipes_data.get("recipes", []), list):
        print(f"错误: recipes.json 的 'recipes' 不是列表，类型: {type(recipes_data.get('recipes'))}")
        return

    # 创建 furniture 的名称到条目的映射
    furniture_map = {item["name"]: item for item in furniture_data["furniture"]}

    # 定义所有可能的前缀
    prefixes = ["配方：", "蓝图：", "设计：", "配方图", "制作图：", "图纸："]

    # 统计更新计数
    updated_count = 0

    # 遍历 recipes，寻找包含指定前缀的条目
    for recipe in recipes_data["recipes"]:
        recipe_name = recipe.get("name", "")
        # 检查是否以任一前缀开头
        for prefix in prefixes:
            if recipe_name.startswith(prefix):
                # 提取去掉前缀后的名称
                base_name = recipe_name[len(prefix):]
                furniture_item = furniture_map.get(base_name)
                if furniture_item:
                    # 检查 furniture 中 ingredients 是否为空
                    if not furniture_item.get("ingredients", "").strip():
                        # 复制 recipes 中的 ingredients 和 canBeCrafted
                        furniture_item["ingredients"] = recipe.get("ingredients", "")
                        furniture_item["canBeCrafted"] = True
                        furniture_item["skills"] = recipe.get("skills", "")
                        furniture_item["type"] = recipe.get("type", "")
                        updated_count += 1
                        print(f"更新家具: {base_name}, 新增材料: {furniture_item['ingredients']}, 可制作: {furniture_item['canBeCrafted']}")
                    else:
                        print(f"跳过 {base_name}: ingredients 已存在 ({furniture_item['ingredients']})")
                else:
                    print(f"未在 furniture.json 中找到匹配的家具: {base_name}")
                break  # 找到匹配的前缀后退出前缀循环

    # 保存更新后的 furniture 数据
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(furniture_data, f, ensure_ascii=False, indent=2)
        print(f"更新完成，修改了 {updated_count} 个家具的 ingredients 和 canBeCrafted，输出到 {output_file}")
    except Exception as e:
        print(f"写入 furniture.json 出错: {e}")
        
def main():
    base_path = Path("C:/projects/ESOCN")
    cn_lua_file = base_path / "public/data/DataExtractor-cn.lua"
    en_lua_file = base_path / "public/data/DataExtractor-en.lua"
    export_json_file = base_path / "public/data/exportJson.json"
    output_dir = base_path / "src/Data"
    
    # 获取 LUA 文件修改时间
    cn_mtime = os.path.getmtime(cn_lua_file)
    en_mtime = os.path.getmtime(en_lua_file)
    print(f"中文 Lua 文件修改时间: {cn_mtime}")
    print(f"英文 Lua 文件修改时间: {en_mtime}")
    
    # 检查输出 JSON 文件的时间戳
    categories = ["equipment", "foods", "collectibleFurniture", "furniture", "cpSkills", "skills", "recipes"]  # 添加 "recipes"
    all_json_fresh = True
    for category in categories:
        json_file = output_dir / f"{category}.json"
        if not json_file.exists():
            print(f"{category}.json 不存在，将生成")
            all_json_fresh = False
            break
        json_mtime = os.path.getmtime(json_file)
        if json_mtime < cn_mtime or json_mtime < en_mtime:
            print(f"{category}.json 已过期，将重新生成")
            all_json_fresh = False
            break
    
    if all_json_fresh:
        print("所有 JSON 文件均为最新，跳过处理")
        return
    
    # 读取 exportJson 文件
    try:
        with open(export_json_file, "r", encoding="utf-8") as f:
            export_json = json.load(f)
    except Exception as e:
        print(f"读取 exportJson.json 出错: {e}")
        return
    
    # 读取并解析 LUA 文件
    try:
        cn_data = luadata.unserialize(cn_lua_file.read_text(encoding="utf-8"))
        en_data = luadata.unserialize(en_lua_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"解析 LUA 文件出错: {e}")
        return
    
    # 处理每个类别
    processors = {
        "equipment": process_sets,
        "foods": process_foods,
        "collectibleFurniture": process_collectible_furniture,
        "furniture": process_furniture,
        "cpSkills": lambda cn, en: process_cp_skills(cn, en, export_json),
        "skills": process_skills,
        "recipes": process_recipes  # 添加 recipes 处理
    }
    
    for category, processor in processors.items():
        json_file = output_dir / f"{category}.json"
        json_mtime = os.path.getmtime(json_file) if json_file.exists() else 0
        
        if json_mtime >= cn_mtime and json_mtime >= en_mtime:
            print(f"{category}: 时间戳匹配，跳过 JSON 生成")
            continue
        
        try:
            data = processor(cn_data, en_data)
            output_data = {
                "timestamp": str(uuid4()),
                category.lower() if category not in ["cpSkills", "skills"] else "skills": data
            }
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"{category} JSON 文件生成成功，包含 {len(data)} 项")
        except Exception as e:
            print(f"处理 {category} 出错: {e}")
    merge_food_ingredients()
    merge_furniture_ingredients()

if __name__ == "__main__":
    main()