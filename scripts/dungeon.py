import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import json
import pymysql
import time
import hashlib
import uuid
import re

# 设置请求头，模拟浏览器
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 根页面 URL
root_url = "https://en.uesp.net/wiki/Online:Group_Dungeons"
base_url = "https://en.uesp.net"

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

async def youdaoTranslate(translate_text, flag=0):
    '''
    :param translate_text: 待翻译的句子
    :param flag: 1:原句子翻译成英文；0:原句子翻译成中文
    :return: 返回翻译结果
    '''
    return translate_text
    
    youdao_url = 'https://openapi.youdao.com/api'
    input_text = ""
    if len(translate_text) <= 20:
        input_text = translate_text
    elif len(translate_text) > 20:
        input_text = translate_text[:10] + str(len(translate_text)) + translate_text[-10:]
    time_curtime = int(time.time())
    app_id = "1d953d33718efa0d"
    uu_id = uuid.uuid4()
    app_key = "1pwz6jOTBEqzjA48jWzAjfGzLryrSxqm"
    sign = hashlib.sha256((app_id + input_text + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()
    data = {
        'q': translate_text,
        'appKey': app_id,
        'salt': uu_id,
        'sign': sign,
        'signType': "v3",
        'curtime': time_curtime,
    }
    if flag:
        data['from'] = "zh-CHS"
        data['to'] = "en"
    else:
        data['from'] = "en"
        data['to'] = "zh-CHS"
    r = requests.get(youdao_url, params=data).json()
    print(r["translation"][0])
    return r["translation"][0]

# 获取技能图标
def fetch_skill_icon(en_name):
    search_term = en_name.replace(" ", "+")
    url = f"https://esoitem.uesp.net/viewlog.php?search={search_term}&searchtype=minedSkills"
    try:
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth("esolog", "esolog"), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            print(f"未找到表格: {url}")
            return "https://esoicons.uesp.net/esoui/art/icons/ability_mage_065.png"
        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                td = cols[2]
                a_tag = td.find("a", href=True)
                if a_tag and a_tag["href"] != "//esoicons.uesp.net/esoui/art/icons/ability_mage_065.png":
                    return "https:" + a_tag["href"]
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
                                if full_img_div:
                                    full_img_link = full_img_div.find("a", href=True)
                                    if full_img_link:
                                        dungeon["DLCicon"] = "https:" + full_img_link["href"]
                crawl_detail_page(dungeon_url, dungeon)
                await translate_dungeon(dungeon)
                print(json.dumps(dungeon, ensure_ascii=False))
                dungeons_data.append(dungeon)

# 爬取 BOSS 页面的函数
def crawl_boss_page(url, boss):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 提取 des
        content = soup.find("div", class_="mw-parser-output")
        if content:
            paragraphs = []
            for element in content.children:
                if element.name == "h2":
                    break
                if element.name == "p":
                    text = re.sub(r'[\n\xa0]+', ' ', element.get_text(separator="", strip=False)).strip()
                    if text:
                        paragraphs.append(text)
            if paragraphs:
                boss["des"] = "\n".join(paragraphs)

        # 提取 BOSS picture
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
                    current_header = re.sub(r'[\n\xa0]+', ' ', header.get_text(strip=False)).strip()
                    if (value and current_header == "Species") or (value and current_header == "Race"):
                        boss["spicies"] = re.sub(r'[\n\xa0]+', ' ', value.get_text(strip=False)).strip()
                    elif value and current_header == "Health":
                        health_texts = []
                        for content in value.contents:
                            if isinstance(content, str):
                                text = re.sub(r'[\n\xa0]+', ' ', content).strip()
                                text = re.sub(r'\s*\(Hard\s*Mode\)', '', text, flags=re.IGNORECASE)
                                if text and text.replace(",", "").isdigit():
                                    health_texts.append(text)
                        if health_texts:
                            boss["n-Health"] = health_texts[0] if len(health_texts) > 0 else ""
                            boss["v-Health"] = health_texts[1] if len(health_texts) > 1 else ""
                            boss["hmHealth"] = health_texts[2] if len(health_texts) > 2 else ""

        # 提取 Skills and Abilities
        skills_header = None
        for h2 in soup.find_all("h2"):
            h2_text = re.sub(r'[\n\xa0]+', ' ', h2.get_text(strip=False)).strip()
            if "Skills and Abilities" in h2_text or "Skills & Abilities" in h2_text:
                skills_header = h2
                break

        if skills_header:
            next_h2 = skills_header.find_next("h2")
            skills = []
            current = skills_header.next_sibling
            while current and (not next_h2 or current != next_h2):
                if current.name == "dl":
                    # 检查嵌套的 <dl>
                    nested_dls = current.find_all("dl", recursive=False)
                    if nested_dls:
                        for dl in nested_dls:
                            dt = dl.find("dt")
                            if dt:
                                # 移除 <sup> 标签
                                for sup in dt.find_all("sup"):
                                    sup.extract()
                            dd = dl.find("dd")
                            skill = {
                                "name": "",
                                "enName": re.sub(r'[\n\xa0]+', ' ', dt.get_text(strip=False)).strip() if dt else "",
                                "icon": "",
                                "des": re.sub(r'[\n\xa0]+', ' ', dd.get_text(separator="", strip=False)).strip() if dd else ""
                            }
                            if skill["enName"]:
                                skill["icon"] = fetch_skill_icon(skill["enName"])
                            skills.append(skill)
                    else:
                        # 处理当前 <dl> 中的所有 <dt> 和 <dd> 组合
                        dt_dd_pairs = current.find_all(["dt", "dd"])
                        i = 0
                        while i < len(dt_dd_pairs) - 1:
                            if dt_dd_pairs[i].name == "dt" and dt_dd_pairs[i + 1].name == "dd":
                                dt = dt_dd_pairs[i]
                                # 移除 <sup> 标签
                                for sup in dt.find_all("sup"):
                                    sup.extract()
                                dd = dt_dd_pairs[i + 1]
                                skill = {
                                    "name": "",
                                    "enName": re.sub(r'[\n\xa0]+', ' ', dt.get_text(strip=False)).strip() if dt else "",
                                    "icon": "",
                                    "des": re.sub(r'[\n\xa0]+', ' ', dd.get_text(separator="", strip=False)).strip() if dd else ""
                                }
                                if skill["enName"]:
                                    skill["icon"] = fetch_skill_icon(skill["enName"])
                                skills.append(skill)
                                i += 2
                            else:
                                i += 1
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

        infobox = soup.find("table", class_="wikitable infobox")
        if infobox:
            rows = infobox.find_all("tr")
            current_header = None
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header:
                    current_header = re.sub(r'[\n\xa0]+', ' ', header.get_text(strip=False)).strip()
                    if value:
                        value_text = re.sub(r'[\n\xa0]+', ' ', value.get_text(strip=False)).strip()
                        if current_header == "Min Level":
                            dungeon["mini_level"] = value_text
                        elif current_header == "Group Size":
                            dungeon["Group_Size"] = value_text
                        elif current_header == "Bosses":
                            dungeon["Bosses"] = value_text
                        elif current_header == "Mini-Bosses":
                            dungeon["mini_Bosses"] = value_text
                elif value and current_header:
                    value_text = re.sub(r'[\n\xa0]+', ' ', value.get_text(strip=False)).strip()
                    if current_header == "Zone":
                        dungeon["enplace"] = [z.strip() for z in value_text.split(",")]
                    elif current_header == "Location":
                        dungeon["location"] = value_text
                    elif current_header == "Loading Screen":
                        for div in value.find_all("div"):
                            style = div.get("style", "")
                            if "text-align" in style and "center" in style:
                                italic = div.find("i")
                                if italic:
                                    mystery_text = re.sub(r'[\n\xa0]+', ' ', "".join(italic.find_all(string=True, recursive=False))).strip()
                                    dungeon["mystery"] = mystery_text
                                    break
                        img_link = value.find("a", href=True)
                        if img_link and "/wiki/File:" in img_link["href"]:
                            img_page_url = base_url + img_link["href"]
                            img_page = requests.get(img_page_url, headers=headers).text
                            img_soup = BeautifulSoup(img_page, "html.parser")
                            full_img_div = img_soup.find("div", class_="fullImageLink")
                            if full_img_div:
                                full_img_link = full_img_div.find("a", href=True)
                                if full_img_link:
                                    dungeon["background"] = "https:" + full_img_link["href"]

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
                        dungeon["picture"] = "https:" + full_img_link["href"]

        content = soup.find("div", class_="mw-parser-output")
        if content:
            paragraphs = []
            for element in content.children:
                if element.name == "h2":
                    break
                if element.name == "p":
                    text = re.sub(r'[\n\xa0]+', ' ', element.get_text(strip=False)).strip()
                    if text:
                        paragraphs.append(text)
            if paragraphs:
                dungeon["des"] = "\n".join(paragraphs)

            bosses_header = None
            for h3 in content.find_all("h3"):
                headline = h3.find("span", class_="mw-headline")
                if headline and re.sub(r'[\n\xa0]+', ' ', headline.get_text(strip=False)).strip().lower() == "bosses":
                    bosses_header = h3
                    break
            if bosses_header:
                next_element = bosses_header.find_next()
                while next_element and next_element.name != "ul" and next_element.name != "h3":
                    next_element = next_element.find_next()
                if next_element and next_element.name == "ul":
                    boss_items = next_element.find_all("li")
                    for item in boss_items:
                        first_link = item.find("a")
                        en_name = re.sub(r'[\n\xa0]+', ' ', first_link.get_text(strip=False)).strip() if first_link else item.get_text(strip=False)
                        boss = {
                            "name": "",
                            "enName": en_name,
                            "spicies": "",
                            "place": dungeon["enName"],
                            "n-Health": "",
                            "v-Health": "",
                            "hmHealth": "",
                            "des": "",
                            "picture": "",
                            "skills": []
                        }
                        if first_link and "/wiki/Online:" in first_link["href"]:
                            boss_url = base_url + first_link["href"]
                            crawl_boss_page(boss_url, boss)
                        dungeon["BOSS"].append(boss)

            sets_header = None
            for h2 in content.find_all("h2"):
                if "Sets" in re.sub(r'[\n\xa0]+', ' ', h2.get_text(strip=False)).strip():
                    sets_header = h2
                    break
            if sets_header:
                table = sets_header.find_next("table", class_="wikitable")
                if table:
                    rows = table.find_all("tr")[1:]
                    for row in rows:
                        th = row.find("th")
                        if th:
                            dungeon["equipment"].append(re.sub(r'[\n\xa0]+', ' ', th.get_text(strip=False)).strip())

            achievements_header = None
            for h2 in content.find_all("h2"):
                if "Achievements" in re.sub(r'[\n\xa0]+', ' ', h2.get_text(strip=False)).strip():
                    achievements_header = h2
                    break
            if achievements_header:
                table = achievements_header.find_next("table", class_="wikitable")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        tds = row.find_all("td")
                        if len(tds) >= 4:
                            achievement = {
                                "name": "",
                                "enName": tds[1].find("a").get_text(strip=False) if tds[1].find("a") else tds[1].get_text(strip=False),
                                "icon": "",
                                "des": re.sub(r'[\n\xa0]+', ' ', tds[3].get_text(separator="", strip=False)).strip(),
                                "score": re.sub(r'[\n\xa0]+', ' ', tds[2].get_text(strip=False)).strip()
                            }
                            img_link = tds[0].find_all("a", href=True)[1] if len(tds[0].find_all("a", href=True)) > 1 else tds[0].find("a", href=True)
                            if img_link and "/wiki/File:" in img_link["href"]:
                                img_page_url = base_url + img_link["href"]
                                img_page = requests.get(img_page_url, headers=headers).text
                                img_soup = BeautifulSoup(img_page, "html.parser")
                                full_img_div = img_soup.find("div", class_="fullImageLink")
                                if full_img_div:
                                    full_img_link = full_img_div.find("a", href=True)
                                    if full_img_link:
                                        achievement["icon"] = "https:" + full_img_link["href"]
                            dungeon["achievement"].append(achievement)

        print(f"已爬取: {dungeon['enName']}")
    except Exception as e:
        print(f"爬取 {url} 失败: {e}")

# 翻译处理函数
async def translate_dungeon(dungeon):
    for place in dungeon["enplace"]:
        zhplace = query_zh_text(place)
        if place:
            dungeon["place"].append(zhplace)
    zh_name = query_zh_text(dungeon["enName"])
    if zh_name:
        dungeon["name"] = zh_name
    if dungeon["mystery"]:
        zh_mystery = query_zh_text(dungeon["mystery"])
        if zh_mystery:
            dungeon["mystery"] = zh_mystery
    if dungeon["des"]:
        dungeon["des"] = await youdaoTranslate(dungeon["des"])
    for boss in dungeon["BOSS"]:
        zh_boss_name = query_zh_text(boss["enName"])
        if zh_boss_name:
            boss["name"] = zh_boss_name
        if boss["spicies"]:
            zh_spicies = query_zh_text(boss["spicies"])
            if zh_spicies:
                boss["spicies"] = zh_spicies
        if boss["des"]:
            boss["des"] = await youdaoTranslate(boss["des"])
        for skill in boss["skills"]:
            zh_skill_name = query_zh_text(skill["enName"])
            if zh_skill_name:
                skill["name"] = zh_skill_name
            if skill["des"]:
                skill["des"] = await youdaoTranslate(skill["des"])
    for achievement in dungeon["achievement"]:
        zh_ach_name = query_zh_text(achievement["enName"])
        if zh_ach_name:
            achievement["name"] = zh_ach_name
        if achievement["des"]:
            zh_ach_des = query_zh_text(achievement["des"])
            if zh_ach_des:
                achievement["des"] = zh_ach_des

async def main():
    print("爬取 Base Game Dungeons...")
    await process_table(base_game_table, is_dlc=False)
    print("爬取 DLC Dungeons...")
    await process_table(dlc_table, is_dlc=True)
    with open("group_dungeons.json", "w", encoding="utf-8") as f:
        json.dump(dungeons_data, f, ensure_ascii=False, indent=4)
    print("爬取完成，已生成 group_dungeons.json")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())