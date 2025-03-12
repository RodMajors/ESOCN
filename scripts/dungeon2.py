import requests
from bs4 import BeautifulSoup
import json
import pymysql
import time
import hashlib
import uuid
import deepl
from deepl.exceptions import TooManyRequestsException

# 设置请求头，模拟浏览器
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 根页面 URL
root_url = "https://en.uesp.net/wiki/Online:Group_Dungeons"
base_url = "https://en.uesp.net"

# 初始化 Google Translate

# 数据库连接信息
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lzr@136595755",
    "database": "esodata",
    "port": 3306,
    "charset": "utf8mb4"
}

# 数据库连接函数
def connect_db():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.Error as e:
        print(f"数据库连接失败: {e}")
        raise
import deepl

import deepl
import asyncio

# async def youdaoTranslate(strs):
#     auth_key = "28a6ff26-3dd0-471a-a7d9-2515755d00d9"  # 使用 DeepL 免费 API
#     target_language = 'ZH'  # 目标语言为中文
#     translator = deepl.Translator(auth_key)  # 初始化 DeepL 翻译器

#     retries = 3  # 重试次数
#     delay = 5  # 每次重试的延迟时间（秒）

#     for attempt in range(retries):
#         try:
#             # 使用异步方式调用 DeepL API
#             result = await asyncio.to_thread(translator.translate_text, strs, target_lang=target_language)
#             print(result.text)
#             return result.text
#         except TooManyRequestsException:
#             print(f"请求过多，等待 {delay} 秒后重试... (尝试 {attempt + 1}/{retries})")
#             await asyncio.sleep(delay)  # 等待一段时间后重试
#         except Exception as e:
#             print(f"翻译失败: {e}")
#             return strs  # 如果翻译失败，返回原始文本

#     print(f"重试 {retries} 次后仍失败，返回原始文本")
#     return strs  # 如果重试多次仍失败，返回原始文本



# 查询数据库函数
def query_zh_text(en_text):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT zhText FROM esotext WHERE enText = %s LIMIT 1", (en_text,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except pymysql.Error as e:
        print(f"查询失败: {e}")
        return None


async def youdaoTranslate(translate_text,flag=0):
    '''
    :param translate_text: 待翻译的句子
    :param flag: 1:原句子翻译成英文；0:原句子翻译成中文
    :return: 返回翻译结果
    '''
    youdao_url = 'https://openapi.youdao.com/api'  # 有道api地址

    # 翻译文本生成sign前进行的处理
    input_text = ""

    # 当文本长度小于等于20时，取文本
    if (len(translate_text) <= 20):
        input_text = translate_text

    # 当文本长度大于20时，进行特殊处理
    elif (len(translate_text) > 20):
        input_text = translate_text[:10] + str(len(translate_text)) + translate_text[-10:]

    time_curtime = int(time.time())  # 秒级时间戳获取
    app_id = "1d953d33718efa0d"  # 自己的应用id
    uu_id = uuid.uuid4()  # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = "1pwz6jOTBEqzjA48jWzAjfGzLryrSxqm"  # 自己的应用密钥

    sign = hashlib.sha256(
        (app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()  # sign生成

    data = {
        'q': translate_text,  # 翻译文本
        'appKey': app_id,  # 应用id
        'salt': uu_id,  # 随机生产的uuid码
        'sign': sign,  # 签名
        'signType': "v3",  # 签名类型，固定值
        'curtime': time_curtime,  # 秒级时间戳
    }
    if flag:
        data['from'] = "zh-CHS"  # 译文语种
        data['to'] = "en"  # 译文语种
    else:
        data['from'] = "en"  # 译文语种
        data['to'] = "zh-CHS"  # 译文语种

    r = requests.get(youdao_url, params=data).json()  # 获取返回的json()内容
    # print("翻译后的结果：" + r["translation"][0])  # 获取翻译内容
    print(r["translation"][0])
    return r["translation"][0]
    

# 获取技能图标
def fetch_skill_icon(en_name):
    # 构造 URL
    search_term = en_name.replace(" ", "+")
    url = f"https://chat.uesp.net/esolog/viewlog.php?search={search_term}&searchtype=minedSkills"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)  # 设置超时避免卡死
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 找到唯一的表格
        table = soup.find("table")
        if not table:
            print(f"未找到表格: {url}")
            return "https://esoicons.uesp.net/esoui/art/icons/ability_mage_065.png"
        
        # 获取第三列（icon 列）的所有 <td>
        rows = table.find_all("tr")[1:]  # 跳过表头
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:  # 确保有第三列
                td = cols[2]  # 第三列是 icon
                a_tag = td.find("a", href=True)
                if a_tag and a_tag["href"] != "//esoicons.uesp.net/esoui/art/icons/ability_mage_065.png":
                    return "https:" + a_tag["href"]
        
        # 如果没有找到合适的图标，返回默认值
        return "https://esoicons.uesp.net/esoui/art/icons/ability_mage_065.png"
    
    except Exception as e:
        print(f"获取技能图标失败 {url}: {e}")
        return "https://esoicons.uesp.net/esoui/art/icons/ability_mage_065.png"

# 发送请求并解析根页面
response = requests.get(root_url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# 存储所有地下城数据
dungeons_data = []

# 找到两个表格（Base Game 和 DLC）
tables = soup.find_all("table", class_="wikitable")
base_game_table = tables[0]
dlc_table = tables[1]

# 处理表格的通用函数
async def process_table(table, is_dlc=False):
    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            dungeon_link = cols[0].find("a")
            if dungeon_link:
                en_name = dungeon_link.get_text(strip=False)
                dungeon_url = base_url + dungeon_link["href"]
                dungeon = {
                    "name": "",
                    "enName": en_name,
                    "place": [],
                    "enplace": [],
                    "DLC": "本体" if not is_dlc else "",
                    "DLCicon": "https://images.uesp.net/a/a3/ON-Icon-Transparent_Logo.png" if not is_dlc else "",
                    "location": "",
                    "mini_level": "",
                    "Group_Size": "",
                    "Bosses": "",
                    "mini_Bosses": "",
                    "background": "",
                    "picture": "",
                    "mystery": "",
                    "des": "",
                    "BOSS": [],
                    "equipment": [],
                    "achievement": [],
                    "drop": [],
                    "mech": []
                }
                if is_dlc:
                    th = row.find("th")
                    if th:
                        dlc_link = th.find("a")
                        if dlc_link:
                            dungeon["DLC"] = dlc_link.get_text(strip=False)
                        div = th.find("div")
                        if div:
                            img_link = div.find("a", href=True)
                            if img_link and "/wiki/File:" in img_link["href"]:
                                img_page_url = base_url + img_link["href"]
                                img_page = requests.get(img_page_url, headers=headers).text
                                img_soup = BeautifulSoup(img_page, "html.parser")
                                full_img_div = img_soup.find("div", class_="fullImageLink")
                                # if full_img_div:
                                #     full_img_link = full_img_div.find("a", href=True)
                                #     if full_img_link:
                                #         dungeon["DLCicon"] = "https:" + full_img_link["href"]
                crawl_detail_page(dungeon_url, dungeon)
                await translate_dungeon(dungeon)  # 使用 await 调用异步函数
                print(dungeon)
                dungeons_data.append(dungeon)

# 爬取 BOSS 页面的函数
def crawl_boss_page(url, boss):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # # 提取 des
        content = soup.find("div", class_="mw-parser-output")
        if content:
            paragraphs = []
            for element in content.children:
                if element.name == "h2":
                    break
                if element.name == "p":
                    text = element.get_text(separator="", strip=False)
                    if text:
                        paragraphs.append(text)
            if paragraphs:
                boss["des"] = "\n".join(paragraphs)

        # # 提取 BOSS picture
        top_img_div = soup.find("div", class_="thumbinner")
        if top_img_div:
            img_link = top_img_div.find("a", href=True)
            if img_link:
                img_page_url = base_url + img_link["href"]
                img_page = requests.get(img_page_url, headers=headers).text
                img_soup = BeautifulSoup(img_page, "html.parser")
                full_img_div = img_soup.find("div", class_="fullImageLink")
                if full_img_div:
                    full_img_link = full_img_div.find("a", href=True)
                    if full_img_link:
                        boss["picture"] = "https:" + full_img_link["href"]

        # 找到右侧信息框
        infobox = soup.find("table", class_="wikitable infobox")
        if infobox:
            rows = infobox.find_all("tr")
            current_header = None
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header:
                    current_header = header.get_text(strip=False)
                    if value and (current_header == 'Race' or current_header == 'Species'):
                        boss["species"] = value.get_text(strip=False)
                    elif value and current_header == "Health":
                        health_texts = []
                        for content in value.contents:
                            if isinstance(content, str):
                                text = content.strip(" (Hardmode)")
                                if text and text.replace(",", "").isdigit():
                                    health_texts.append(text)
                        if health_texts:
                            boss["n-Health"] = health_texts[0] if len(health_texts) > 0 else ""
                            boss["v-Health"] = health_texts[1] if len(health_texts) > 1 else ""
                            boss["hmHealth"] = health_texts[2] if len(health_texts) > 2 else ""

        # 提取 Skills and Abilities
        skills_header = None
        for h2 in soup.find_all("h2"):
            if "Skills and Abilities" in h2.get_text(strip=False):
                skills_header = h2
                break

        if skills_header:
            next_h2 = skills_header.find_next("h2")
            skills = []
            current = skills_header.next_sibling
            while current and (not next_h2 or current != next_h2):
                if current.name == "dl":
                    nested_dls = current.find_all("dl", recursive=False)
                    if nested_dls:
                        for dl in nested_dls:
                            dts = dl.find_all("dt")
                            dds = dl.find_all("dd")
                            for dt, dd in zip(dts, dds):
                                skill = {
                                    "name": "",
                                    "enName": dt.get_text(strip=False) if dt else "",
                                    "icon": "",
                                    "des": dd.get_text(separator="", strip=False) if dd else ""
                                }
                                if skill["enName"]:
                                    skill["icon"] = fetch_skill_icon(skill["enName"])
                                skills.append(skill)
                    else:
                        dts = current.find_all("dt")
                        dds = current.find_all("dd")
                        for dt, dd in zip(dts, dds):
                            skill = {
                                "name": "",
                                "enName": dt.get_text(strip=False) if dt else "",
                                "icon": "",
                                "des": dd.get_text(separator="", strip=False) if dd else ""
                            }
                            if skill["enName"]:
                                skill["icon"] = fetch_skill_icon(skill["enName"])
                            skills.append(skill)
                current = current.next_sibling
            boss["skills"].extend(skills)
        print(f"已爬取 BOSS: {boss['enName']}")
    except Exception as e:
        print(f"爬取 BOSS {url} 失败: {e}")

# 爬取详情页的函数
def crawl_detail_page(url, dungeon):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        content = soup.find("div", class_="mw-parser-output")
        if content:
            paragraphs = []
            # for element in content.children:
            #     if element.name == "h2":
            #         break
            #     if element.name == "p":
            #         text = element.get_text(separator="", strip=False)
            #         if text:
            #             paragraphs.append(text)
            # if paragraphs:
            #     dungeon["des"] = "\n".join(paragraphs)

            # bosses_header = None
            # for h3 in content.find_all("h3"):
            #     headline = h3.find("span", class_="mw-headline")
            #     if headline and headline.get_text(strip=False).lower() == "minibosses":
            #         bosses_header = h3
            #         break
            # if bosses_header:
            #     next_element = bosses_header.find_next()
            #     while next_element and next_element.name != "ul" and next_element.name != "h3":
            #         next_element = next_element.find_next()
            #     if next_element and next_element.name == "ul":
            #         boss_items = next_element.find_all("li")
            #         for item in boss_items:
            #             first_link = item.find("a")
            #             en_name = first_link.get_text(strip=False) if first_link else item.get_text(strip=False)
            #             boss = {
            #                 "name": "",
            #                 "enName": en_name,
            #                 "species": "",
            #                 "place": dungeon["enName"],
            #                 "n-Health": "",
            #                 "v-Health": "",
            #                 "hmHealth": "",
            #                 "des": "",
            #                 "picture": "",
            #                 "skills": []
            #             }
            #             if first_link and "/wiki/Online:" in first_link["href"]:
            #                 boss_url = base_url + first_link["href"]
            #                 crawl_boss_page("https://en.uesp.net/wiki/Online:Sister_Gohlla", boss)
            #                 crawl_boss_page("https://en.uesp.net/wiki/Online:Sister_Hiti", boss)
            #                 crawl_boss_page("https://en.uesp.net/wiki/Online:Sister_Bani", boss)
            #                 crawl_boss_page("https://en.uesp.net/wiki/Online:Sister_Maefyn", boss)
            #                 crawl_boss_page("https://en.uesp.net/wiki/Online:Mother_Ciannait", boss)
            #             dungeon["BOSS"].append(boss)
            dungeon["enName"] = "冰境"
            boss1 = {
                "name": "",
                "enName": "Eliam Merick",
                "species": "",
                "place": dungeon["enName"],
                "n-Health": "",
                "v-Health": "",
                "hmHealth": "",
                "des": "",
                "picture": "",
                "skills": []
            }
            boss2 = {
                "name": "",
                "enName": "Liramindrel",
                "species": "",
                "place": dungeon["enName"],
                "n-Health": "",
                "v-Health": "",
                "hmHealth": "",
                "des": "",
                "picture": "",
                "skills": []
            }
            boss3 = {
                "name": "",
                "enName": "Ihudir",
                "species": "",
                "place": dungeon["enName"],
                "n-Health": "",
                "v-Health": "",
                "hmHealth": "",
                "des": "",
                "picture": "",
                "skills": []
            }
            boss4 = {
                "name": "",
                "enName": "Sister Maefyn",
                "species": "",
                "place": dungeon["enName"],
                "n-Health": "",
                "v-Health": "",
                "hmHealth": "",
                "des": "",
                "picture": "",
                "skills": []
            }
            boss5 = {
                "name": "",
                "enName": "Mother Ciannait",
                "species": "",
                "place": dungeon["enName"],
                "n-Health": "",
                "v-Health": "",
                "hmHealth": "",
                "des": "",
                "picture": "",
                "skills": []
            }
            crawl_boss_page("https://en.uesp.net/wiki/Online:Eliam_Merick", boss1)
            dungeon["BOSS"].append(boss1)
            crawl_boss_page("https://en.uesp.net/wiki/Online:Liramindrel", boss2)
            dungeon["BOSS"].append(boss2)
            crawl_boss_page("https://en.uesp.net/wiki/Online:Ihudir", boss3)
            dungeon["BOSS"].append(boss3)
            # crawl_boss_page("https://en.uesp.net/wiki/Online:Sister_Maefyn", boss4)
            # dungeon["BOSS"].append(boss4)
            # crawl_boss_page("https://en.uesp.net/wiki/Online:Mother_Ciannait", boss5)
            # dungeon["BOSS"].append(boss5)
            sets_header = None
            for h2 in content.find_all("h2"):
                if "Sets" in h2.get_text(strip=False):
                    sets_header = h2
                    break
            if sets_header:
                table = sets_header.find_next("table")
                if table:
                    rows = table.find_all("tr")[1:]
                    for row in rows:
                        th = row.find("th")
                        if th:
                            dungeon["equipment"].append(th.get_text(strip=False))

        print(f"已爬取: {dungeon['enName']}")
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")

# 翻译处理函数
async def translate_dungeon(dungeon):
    if dungeon["des"]:
        dungeon["des"] = await youdaoTranslate(dungeon["des"])
    # 翻译 BOSS
    for boss in dungeon["BOSS"]:
        # 翻译 name（仍使用数据库）
        zh_boss_name = query_zh_text(boss["enName"])
        if zh_boss_name:
            boss["name"] = zh_boss_name
        # 翻译 species（仍使用数据库）
        if boss["species"]:
            zh_species = query_zh_text(boss["species"])
            if zh_species:
                boss["species"] = zh_species
            else:
                boss["species"] = await youdaoTranslate(boss["species"])
        # 翻译 boss["des"]（使用有道翻译）
        if boss["des"]:
            boss["des"] = await youdaoTranslate(boss["des"])
        # 翻译 skills
        for skill in boss["skills"]:
            zh_skill_name = query_zh_text(skill["enName"])
            if zh_skill_name:
                skill["name"] = zh_skill_name
            else:
                skill["name"] = await youdaoTranslate(skill["enName"])
            # 翻译 skill["des"]（使用有道翻译）
            if skill["des"]:
                skill["des"] = await youdaoTranslate(skill["des"])

async def main():
    print("爬取 Base Game Dungeons...")
    await process_table(base_game_table, is_dlc=False)
    print("爬取 DLC Dungeons...")
    await process_table(dlc_table, is_dlc=True)

    # 保存为 JSON 文件
    with open("group_dungeons.json", "w", encoding="utf-8") as f:
        json.dump(dungeons_data, f, ensure_ascii=False, indent=4)

    print("爬取完成，已生成 group_dungeons.json")

# 运行主程序
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())