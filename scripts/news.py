import asyncio
from pyppeteer import launch
import json
import os
import mysql.connector
from datetime import datetime

# 配置
BASE_URL = "https://www.elderscrollsonline.com/cn/news"
DETAIL_URL = "https://www.elderscrollsonline.com/cn/news/post/{}"
OUTPUT_DIR = os.path.join("src", "Data")
NEWS_LIST_PATH = os.path.join(OUTPUT_DIR, "news.json")
LAST_ID_PATH = os.path.join(OUTPUT_DIR, "last-id.txt")
NEWS_HTML_DIR = os.path.join("src", "assets", "news")
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Windows 示例
# CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Mac 示例
# CHROME_PATH = "/usr/bin/google-chrome"  # Linux 示例

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Lzr@136595755",
    "database": "esonews"
}

async def ensure_dirs():
    """确保输出目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(NEWS_HTML_DIR, exist_ok=True)

async def get_last_id():
    """读取上一次爬取的第一个新闻 ID"""
    try:
        with open(LAST_ID_PATH, "r", encoding="utf-8") as f:
            last_id = f.read().strip()
            print(f"Last ID from file: {last_id}")
            return last_id
    except FileNotFoundError:
        print("No last-id.txt found, treating as first run.")
        return None

async def save_last_id(news_id):
    """保存最新的第一个新闻 ID"""
    print(f"Saving new last ID: {news_id}")
    with open(LAST_ID_PATH, "w", encoding="utf-8") as f:
        f.write(news_id)

async def get_news_ids_from_db():
    """从数据库获取所有新闻 ID"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM newsList")
        ids = [row[0] for row in cursor.fetchall()]
        print(f"Retrieved {len(ids)} news IDs from database.")
        cursor.close()
        conn.close()
        return ids
    except Exception as e:
        print(f"Error retrieving news IDs: {e}")
        return []

async def update_database(new_news):
    """更新数据库中的新闻数据"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        for news in new_news:
            cursor.execute("""
                INSERT INTO newsList (id, name, des, cover, date)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name=%s, des=%s, cover=%s, date=%s
            """, (
                news["id"], news["name"], news["des"], news["cover"], news["date"],
                news["name"], news["des"], news["cover"], news["date"]
            ))
        conn.commit()
        print(f"Updated {len(new_news)} news items in database.")
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

async def fetch_news_list():
    """爬取新闻列表"""
    print("Launching browser for news list...")
    browser = await launch(
        headless=True,
        executablePath=CHROME_PATH,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = await browser.newPage()
    
    # 设置 User-Agent 和 headers
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    await page.setExtraHTTPHeaders({
        "Accept-Language": "zh-CN",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": BASE_URL
    })

    # 访问页面并等待渲染
    try:
        print(f"Navigating to {BASE_URL}...")
        await page.goto(BASE_URL, {"waitUntil": "networkidle2", "timeout": 30000})
        # 等待图片元素加载
        await page.waitForSelector('.hilight-image img', {'timeout': 5000})
        # 模拟滚动以触发懒加载
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)  # 等待 2 秒确保图片加载
    except Exception as e:
        print(f"Error loading page: {e}")
        await browser.close()
        return []

    # 提取新闻列表
    news_list = await page.evaluate(r'''() => {
        const articles = document.querySelectorAll(".category-body.row.is-pa.is-pip article.tier-2-list-item");
        return Array.from(articles).map(article => {
            const link = article.querySelector(".link-block a.clean-link");
            const href = link ? link.getAttribute("href") : "";
            const newsId = href ? href.split("/").pop() : "";
            
            const name = link && link.querySelector("h3.text-info") 
                ? link.querySelector("h3.text-info").innerText.trim() 
                : "";
            
            const des = article.querySelector(".link-block p")
                ? article.querySelector(".link-block p").innerText.trim()
                : "";
            
            const date = article.querySelector("p.date")
                ? article.querySelector("p.date").innerText.trim().split(" ")[0]
                : "";
            
            const img = article.querySelector(".hilight-image img");
            let cover = "";
            if (img) {
                cover = (
                    img.getAttribute("data-src") || 
                    img.getAttribute("data-lazy") || 
                    img.getAttribute("data-original") || 
                    img.getAttribute("data-lazyload") || 
                    ""
                );
                if (!cover && img.getAttribute("src") && !img.getAttribute("src").includes("placeholder.jpg")) {
                    cover = img.getAttribute("src");
                }
            }
            const parent = article.querySelector(".hilight-image");
            if (parent) {
                const bgImage = getComputedStyle(parent).backgroundImage;
                if (bgImage && bgImage !== "none") {
                    const urlMatch = bgImage.match(/url\(["']?(.+?)["']?\)/);
                    if (urlMatch && !urlMatch[1].includes("placeholder.jpg")) {
                        cover = urlMatch[1];
                    }
                }
            }
            
            console.log({
                newsId,
                src: img ? img.getAttribute("src") : null,
                dataSrc: img ? img.getAttribute("data-src") : null,
                dataLazy: img ? img.getAttribute("data-lazy") : null,
                dataOriginal: img ? img.getAttribute("data-original") : null,
                dataLazyload: img ? img.getAttribute("data-lazyload") : null,
                backgroundImage: parent ? getComputedStyle(parent).backgroundImage : null,
                cover
            });
            
            return { id: newsId, name, date, des, cover };
        }).filter(item => item.id && item.name && item.date);
    }''')

    print(f"Extracted {len(news_list)} news items.")
    await browser.close()
    return news_list

async def fetch_news_detail(news_id):
    """爬取单个新闻详情页"""
    print(f"Fetching detail for news ID: {news_id}")
    browser = await launch(
        headless=True,
        executablePath=CHROME_PATH,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = await browser.newPage()
    
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    await page.setExtraHTTPHeaders({
        "Accept-Language": "zh-CN",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": BASE_URL
    })

    url = DETAIL_URL.format(news_id)
    try:
        await page.goto(url, {"waitUntil": "networkidle2", "timeout": 30000})
        await page.waitForSelector('.blog-body-wrap', {'timeout': 5000})
        await asyncio.sleep(3)  # 增加等待，确保懒加载完成
    except Exception as e:
        print(f"Error loading detail page {url}: {e}")
        await browser.close()
        return None

    # 提取 blog-body-wrap 内容并处理图片
    content = await page.evaluate('''() => {
        const wrap = document.querySelector(".blog-body-wrap");
        if (!wrap) return "";
        // 处理所有图片
        const images = wrap.querySelectorAll("img");
        images.forEach(img => {
            const lazySrc = img.getAttribute("data-lazy-src");
            if (lazySrc && !lazySrc.includes("placeholder.jpg")) {
                img.setAttribute("src", lazySrc);
                img.removeAttribute("data-lazy-src");
            } else if (img.src.includes("placeholder.jpg")) {
                // 如果没有 data-lazy-src 且 src 是占位符，移除图片
                img.parentNode.removeChild(img);
            }
        });
        return wrap.outerHTML;
    }''')

    # 下载图片（可选）
    download_images = False  # 设置为 True 启用下载
    if download_images:
        async with aiohttp.ClientSession() as session:
            img_urls = re.findall(r'src=["\'](https://esosslfiles-a\.akamaihd\.net/ape/uploads/[^"\']+)["\']', content)
            for img_url in img_urls:
                img_name = img_url.split("/")[-1]
                img_path = os.path.join(NEWS_HTML_DIR, "images", img_name)
                os.makedirs(os.path.join(NEWS_HTML_DIR, "images"), exist_ok=True)
                try:
                    async with session.get(img_url) as resp:
                        if resp.status == 200:
                            with open(img_path, "wb") as f:
                                f.write(await resp.read())
                            content = content.replace(img_url, f"images/{img_name}")
                            print(f"Downloaded image: {img_name}")
                except Exception as e:
                    print(f"Error downloading image {img_url}: {e}")

    await browser.close()
    if not content:
        print(f"No content found for news ID: {news_id}")
        return None

    # 保存 HTML 文件
    html_path = os.path.join(NEWS_HTML_DIR, f"{news_id}.html")
    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n')
            f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write(f'<title>News {news_id}</title>\n</head>\n<body>\n{content}\n</body>\n</html>')
        print(f"Saved HTML for news ID: {news_id} to {html_path}")
        with open(html_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
            if '<div class="blog-body-wrap">' not in saved_content:
                print(f"Warning: blog-body-wrap not found in saved HTML for {news_id}")
        return html_path
    except Exception as e:
        print(f"Error saving HTML for news ID {news_id}: {e}")
        return None
    
async def main():
    print("Starting news crawl...")
    await ensure_dirs()

    # 读取现有新闻列表
    existing_news = []
    if os.path.exists(NEWS_LIST_PATH):
        with open(NEWS_LIST_PATH, "r", encoding="utf-8") as f:
            existing_news = json.load(f)
        print(f"Loaded {len(existing_news)} existing news items.")

    # 读取上一次的第一个新闻 ID
    last_id = await get_last_id()

    # 爬取新闻列表
    try:
        news_list = await fetch_news_list()
    except Exception as e:
        print(f"Error fetching news list: {e}")
        return

    # 如果没有新闻，直接退出
    if not news_list:
        print("No news found.")
        return

    # 保存最新的第一个新闻 ID
    await save_last_id(news_list[0]["id"])

    # 增量爬取：只保留新的新闻（直到遇到 last_id）
    new_news = []
    for news in news_list:
        if last_id and news["id"] == last_id:
            print(f"Reached last known ID: {last_id}. Stopping crawl.")
            break
        new_news.append(news)

    # 如果有新新闻，更新 JSON 和数据库
    if new_news:
        updated_news = [
            news for news in existing_news
            if not any(n["id"] == news["id"] for n in new_news)
        ] + new_news
        with open(NEWS_LIST_PATH, "w", encoding="utf-8") as f:
            json.dump(updated_news, f, ensure_ascii=False, indent=2)
        print(f"Updated news.json with {len(new_news)} new items.")
        await update_database(new_news)
    else:
        print("No new news found.")

    # 爬取数据库中所有新闻的详情页
    news_ids = await get_news_ids_from_db()
    if not news_ids:
        print("No news IDs found in database.")
        return

    for news_id in news_ids:
        html_path = os.path.join(NEWS_HTML_DIR, f"{news_id}.html")
        if os.path.exists(html_path):
            print(f"HTML for news ID {news_id} already exists, skipping.")
            continue
        await fetch_news_detail(news_id)

    print("News crawl completed.")

if __name__ == "__main__":
    asyncio.run(main())