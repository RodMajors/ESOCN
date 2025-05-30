import asyncio
import aiohttp
from pyppeteer import launch
import os
from urllib.parse import urljoin

# 配置
BASE_URL = "https://www.elderscrollsonline.com/cn/news/post/68059"
OUTPUT_DIR = os.path.join("src", "assets", "css")
CSS_PATH = os.path.join(OUTPUT_DIR, "news.css")
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

async def ensure_dirs():
    """确保输出目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

async def fetch_css_file(url):
    """下载单个 CSS 文件内容"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Failed to fetch CSS from {url}: {response.status}")
                    return ""
    except Exception as e:
        print(f"Error fetching CSS from {url}: {e}")
        return ""

async def fetch_page_css():
    """爬取页面中的 CSS 内容"""
    print(f"Fetching CSS from {BASE_URL}")
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
        "Referer": "https://www.elderscrollsonline.com/cn/"
    })

    try:
        await page.goto(BASE_URL, {"waitUntil": "networkidle2", "timeout": 30000})
        await asyncio.sleep(3)  # 等待动态加载
    except Exception as e:
        print(f"Error loading page {BASE_URL}: {e}")
        await browser.close()
        return []

    # 提取 CSS 内容
    css_content = []
    
    # 获取 <link rel="stylesheet">
    try:
        links = await page.evaluate('''() => {
            try {
                return Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                    .map(link => link.href || '');
            } catch (e) {
                console.error('Error in link extraction:', e);
                return [];
            }
        }''')
    except Exception as e:
        print(f"Error evaluating links: {e}")
        links = []

    # 下载 CSS 文件
    for css_url in links:
        if not css_url:
            continue
        absolute_url = urljoin(BASE_URL, css_url)
        css_text = await fetch_css_file(absolute_url)
        if css_text:
            # 过滤相关样式
            relevant_styles = []
            for line in css_text.split('\n'):
                if any(cls in line for cls in ['.blog-body-wrap', '.img-box', '.lead-img', '.button-base', '.tags', '.label']):
                    relevant_styles.append(line)
            if relevant_styles:
                css_content.append(f"/* From {absolute_url} */\n" + "\n".join(relevant_styles) + "\n")

    # 获取 <style> 标签
    try:
        inline_styles = await page.evaluate('''() => {
            try {
                return Array.from(document.querySelectorAll('style'))
                    .map(style => style.textContent || '');
            } catch (e) {
                console.error('Error in style extraction:', e);
                return [];
            }
        }''')
    except Exception as e:
        print(f"Error evaluating inline styles: {e}")
        inline_styles = []

    for style in inline_styles:
        if style.strip():
            relevant_styles = []
            for line in style.split('\n'):
                if any(cls in line for cls in ['.blog-body-wrap', '.img-box', '.lead-img', '.button-base', '.tags', '.label']):
                    relevant_styles.append(line)
            if relevant_styles:
                css_content.append(f"/* Inline style */\n" + "\n".join(relevant_styles) + "\n")

    await browser.close()
    return css_content

async def main():
    await ensure_dirs()
    css_content = await fetch_page_css()
    
    if not css_content:
        print("No CSS content fetched.")
        return

    # 保存 CSS
    try:
        with open(CSS_PATH, "w", encoding="utf-8") as f:
            f.write("/* ESO News CSS - Fetched from elderscrollsonline.com */\n\n")
            f.write("\n".join(css_content))
        print(f"Saved CSS to {CSS_PATH}")
    except Exception as e:
        print(f"Error saving CSS: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            pass  # 忽略事件循环关闭错误
        else:
            raise