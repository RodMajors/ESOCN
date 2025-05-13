import json
import re

def clean_name(name):
    """去除名称中的括号部分"""
    return re.sub(r'\s*\([^)]+\)', '', name).strip()

def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_skills(data):
    """从 DataExtractor 中提取所有技能，展平结构"""
    skills = []
    cp_skills = data.get('Default', {}).get('@RodMajors', {}).get('$AccountWide', {}).get('dataCpSkills', {})
    
    for category in cp_skills.values():
        for skill in category.get('skills', {}).values():
            skill['name'] = clean_name(skill['name'])
            skills.append(skill)
    
    return skills

def merge_skills(data_skills, export_skills):
    """将 DataExtractor 的技能与 exportJson 的指定字段合并，使用 id 和 skillId 匹配"""
    merged_skills = []
    
    # 创建 exportJson 技能的 skillId 查找表
    export_lookup = {skill['skillId']: skill for skill in export_skills}
    
    for data_skill in data_skills:
        merged_skill = data_skill.copy()
        skill_id = str(data_skill['id'])
        
        if skill_id in export_lookup:
            export_skill = export_lookup[skill_id]
            merged_skill['enName'] = export_skill['name']
            merged_skill['maxPoints'] = export_skill['maxPoints']
            merged_skill['jumpPoints'] = export_skill['jumpPoints']
            merged_skill['numJumpPoints'] = export_skill['numJumpPoints']
            merged_skill['jumpPointDelta'] = export_skill['jumpPointDelta']
        
        merged_skills.append(merged_skill)
    
    return merged_skills

def main():
    # 加载 JSON 文件
    data_json = load_json('C:/projects/ESOCN/public/data/DataExtractor.json')
    export_json = load_json('C:/projects/ESOCN/public/data/exportJson.json')
    
    # 从 DataExtractor 提取技能
    data_skills = extract_skills(data_json)
    
    # 获取 exportJson 中的 cp2Skills
    export_skills = export_json.get('cp2Skills', [])
    
    # 合并技能
    merged_skills = merge_skills(data_skills, export_skills)
    
    # 保存合并后的技能到新 JSON 文件
    output = {'skills': merged_skills}
    with open('merged_skills.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()