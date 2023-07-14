import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

import asyncio
from pyppeteer import launch

from setup.setup import connect_to_db
from models.google_search_result import GoogleSearchResult

# 获取网页内容
async def get_page_html(url):
    browser = await launch()
    page = await browser.newPage()

    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    await page.goto(url, timeout=60000)
    await page.waitForSelector('#search')

    html_content = await page.evaluate('''() => {
        return document.querySelector("#search").outerHTML;
    }''')

    await browser.close()

    return html_content

# 保存搜索结果
def save_search_result(url, html_content):
    search_result = GoogleSearchResult(
        search_url=url,
        search_result_html=html_content
    )
    search_result.save()

# 主程序入口
async def main(url):
    connect_to_db()
    html_content = await get_page_html(url)
    save_search_result(url, html_content)

if __name__ == '__main__':
    # 调用主程序
    url = 'https://www.google.com/search?q=final+fantasy+16&num=100'
    asyncio.get_event_loop().run_until_complete(main(url))
