import json
import re

def lua_to_dict(lua_content):
    # 移除Lua文件开头和结尾的无关部分，只保留主要数据结构
    content = lua_content.strip()
    if content.startswith('DataExtractorSavedVariables ='):
        content = content.replace('DataExtractorSavedVariables =', '').strip()
    
    def parse_lua_value(value):
        """处理不同的Lua值类型"""
        value = value.strip()
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '').isdigit() and '.' in value:
            return float(value)
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif value.startswith('|c') and value.endswith('|r'):  # 处理颜色代码
            return value
        return value

    def parse_lua_table(text, start=0):
        """递归解析Lua表结构"""
        result = {}
        i = start
        
        while i < len(text):
            char = text[i]
            
            # 跳过空白字符
            if char.isspace() or char in '\n\r':
                i += 1
                continue
                
            if char == '}':
                return result, i
                
            # 查找键
            key_match = re.match(r'\["([^"]+)"\]\s*=\s*', text[i:])
            if key_match:
                key = key_match.group(1)
                i += key_match.end()
            else:
                num_key_match = re.match(r'\[(\d+)\]\s*=\s*', text[i:])
                if num_key_match:
                    key = int(num_key_match.group(1))
                    i += num_key_match.end()
                else:
                    # 如果没有明确的键，可能是语法错误，跳过
                    i += 1
                    continue

            # 处理值
            if i >= len(text):
                break
                
            if text[i] == '{':
                # 子表
                sub_dict, new_i = parse_lua_table(text, i + 1)
                result[key] = sub_dict
                i = new_i + 1
            elif text[i] == '"':
                # 字符串
                str_match = re.match(r'"([^"]*)"', text[i:])
                if str_match:
                    result[key] = str_match.group(1)
                    i += str_match.end()
                else:
                    i += 1
            else:
                # 其他值（数字、布尔值等）
                value_match = re.match(r'([^,\n}]+)(?=[,\n}]|$)', text[i:])
                if value_match:
                    value = value_match.group(1).strip()
                    result[key] = parse_lua_value(value)
                    i += value_match.end()
                else:
                    i += 1
            
            # 跳过逗号和空格
            while i < len(text) and text[i] in ', \n\r':
                i += 1
                
        return result, i

    try:
        # 找到第一个大括号开始解析
        start_idx = content.index('{')
        parsed_data, _ = parse_lua_table(content, start_idx)
        return parsed_data
    except Exception as e:
        print(f"解析Lua内容时出错: {str(e)}")
        return {}

def convert_lua_to_json(input_path, output_path):
    try:
        # 读取Lua文件
        with open(input_path, 'r', encoding='utf-8') as f:
            lua_content = f.read()
        
        # 转换为Python字典
        data = lua_to_dict(lua_content)
        
        if not data:
            print("警告：转换结果为空字典，请检查输入文件内容")
            print(f"文件开头预览: {lua_content[:100]}")
        
        # 转换为JSON并保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"成功转换文件并保存至: {output_path}")
        
    except Exception as e:
        print(f"转换过程中发生错误: {str(e)}")

# 使用示例
input_file = "C:/projects/ESOCN/public/data/DataExtractor.lua"
output_file = "C:/projects/ESOCN/public/data/DataExtractor.json"

# 如果你想直接测试提供的文本，可以使用以下代码
# lua_text = """你的Lua内容粘贴在这里"""
# with open(input_file, 'w', encoding='utf-8') as f:
#     f.write(lua_text)

convert_lua_to_json(input_file, output_file)