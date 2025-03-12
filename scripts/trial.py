import requests
from bs4 import BeautifulSoup
import json
import pymysql
import time
import hashlib
import uuid
import aiohttp

# 设置请求头，模拟浏览器
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 根页面 URL
root_url = "https://en.uesp.net/wiki/Online:Trials"
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
    print("翻译后的结果：" + r["translation"][0])  # 获取翻译内容
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

trial_data = []

async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def extract_trials(html):
    soup = BeautifulSoup(html, 'html.parser')
    h2_tags = soup.find_all('h2')
    trials = []
    for h2 in h2_tags:
        if h2.text.strip() not in ['Content', 'Notes']:
            ul = h2.find_next('ul')
            if ul:
                for li in ul.find_all('li'):
                    b_tag = li.find('b')
                    if b_tag:
                        a_tag_in_b = b_tag.find('a')
                        if a_tag_in_b:
                            trial_name = a_tag_in_b.text.strip()
                            trial_link = a_tag_in_b.get('href')
                        else:
                            trial_name = b_tag.text.strip()
                            a_tags = li.find_all('a')
                            for a_tag in a_tags:
                                if a_tag.get('href').startswith('/wiki/'):
                                    trial_link = a_tag.get('href')
                                    break
                            else:
                                trial_link = None
                    else:
                        a_tags = li.find_all('a')
                        for a_tag in a_tags:
                            if a_tag.get('href').startswith('/wiki/'):
                                trial_name = a_tag.text.strip()
                                trial_link = a_tag.get('href')
                                break
                        else:
                            continue
                    trials.append({"name": trial_name, "link": trial_link})
    return trials

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
                        # 获取所有文本内容，包括 <br> 分隔的部分
                        full_text = value.get_text(separator=" ", strip=True).split()
                        # 提取数字和可能的 Hard Mode
                        for text in full_text:
                            # 检查是否是纯数字或包含 "(Hard Mode)"
                            if text.replace(",", "").replace("(Hard Mode)", "").isdigit():
                                health_texts.append(text)
                        # 初始化健康值
                        boss["n-Health"] = ""
                        boss["v-Health"] = ""
                        boss["hmHealth"] = ""
                        
                        # 根据内容长度和格式分配健康值
                        for i, health in enumerate(health_texts):
                            if i == 2:
                                boss["hmHealth"] = health.replace(" (Hard Mode)", "")
                            elif i == 0:
                                boss["n-Health"] = health
                            elif i == 1 and not boss["hmHealth"]:
                                boss["v-Health"] = health

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

        infobox = soup.find("table", class_="wikitable infobox")
        if infobox:
            rows = infobox.find_all("tr")
            current_header = None
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if header:
                    current_header = header.get_text(strip=False)
                    if value:
                        value_text = value.get_text(strip=False)
                        if current_header == "Group Size":
                            dungeon["Group_Size"] = value_text
                        elif current_header == "Bosses":
                            dungeon["Bosses"] = value_text
                        elif current_header == "Mini-Bosses":
                            dungeon["mini_Bosses"] = value_text
                elif value and current_header:
                    value_text = value.get_text(strip=False)
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
                                    dungeon["mystery"] = "".join(italic.find_all(string=True, recursive=False)).strip()
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
                    text = element.get_text(separator="", strip=False)
                    if text:
                        paragraphs.append(text)
            if paragraphs:
                dungeon["des"] = "\n".join(paragraphs)

            bosses_header = None
            for h3 in content.find_all("h3"):
                headline = h3.find("span", class_="mw-headline")
                if headline and headline.get_text(strip=False).lower() == "bosses":
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
                        en_name = first_link.get_text(strip=False) if first_link else item.get_text(strip=False)
                        boss = {
                            "name": "",
                            "enName": en_name,
                            "species": "",
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
                if "Sets" in h2.get_text(strip=False):
                    sets_header = h2
                    break
            if sets_header:
                table = sets_header.find_next("table", class_="wikitable")
                if table:
                    rows = table.find_all("tr")[1:]
                    for row in rows:
                        th = row.find("th")
                        if th:
                            dungeon["equipment"].append(th.get_text(strip=False))

            achievements_header = None
            for h2 in content.find_all("h2"):
                if "Achievements" in h2.get_text(strip=False):
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
                                "des": tds[3].get_text(separator="", strip=False),
                                "score": tds[2].get_text(strip=False)
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
    # 翻译 name（仍使用数据库）
    for place in dungeon["enplace"]:
        zhplace = query_zh_text(place)
        if zhplace:
            dungeon["place"].append(zhplace)
        else:
            dungeon["place"].append("")

    zh_name = query_zh_text(dungeon["enName"])
    if zh_name:
        dungeon["name"] = zh_name

    # 翻译 mystery（仍使用数据库）
    if dungeon["mystery"]:
        zh_mystery = query_zh_text(dungeon["mystery"])
        if zh_mystery:
            dungeon["mystery"] = zh_mystery

    # 翻译 dungeon["des"]（使用有道翻译）
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
        # 翻译 boss["des"]（使用有道翻译）
        if boss["des"]:
            boss["des"] = await youdaoTranslate(boss["des"])
        # 翻译 skills
        for skill in boss["skills"]:
            zh_skill_name = query_zh_text(skill["enName"])
            if zh_skill_name != "":
                skill["name"] = zh_skill_name
            else:
                skill["name"] = youdaoTranslate(skill["enName"])
            # 翻译 skill["des"]（使用有道翻译）
            if skill["des"]:
                skill["des"] = await youdaoTranslate(skill["des"])

    # 翻译 achievement（仍使用数据库）
    for achievement in dungeon["achievement"]:
        zh_ach_name = query_zh_text(achievement["enName"])
        if zh_ach_name:
            achievement["name"] = zh_ach_name
        if achievement["des"]:
            zh_ach_des = query_zh_text(achievement["des"])
            if zh_ach_des:
                achievement["des"] = zh_ach_des

async def main():
    url = root_url;
    html = await fetch_page(url)
    trials = await extract_trials(html)
    for trial in trials:
        trialJSON = {
            "name": "",
            "enName": trial['name'],
            "place": [],
            "enplace": [],
            "DLC": "",
            "DLCicon": "",
            "location": "",
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
        crawl_detail_page(base_url+trial['link'], trialJSON)
        await translate_dungeon(trialJSON)
        print(trialJSON)
        trial_data.append(trialJSON)
    with open("group_dungeons.json", "w", encoding="utf-8") as f:
        json.dump(trial_data, f, ensure_ascii=False, indent=4)
        
# 运行主程序
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())