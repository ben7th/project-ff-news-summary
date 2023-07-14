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
    await page.goto(url, timeout=60000, waitUntil='networkidle2')

    html_content = await page.evaluate('''() => {
        return document.querySelector("#main").outerHTML;
    }''')

    result_items_count = await page.evaluate('''() => {
        return document.querySelectorAll('#search h3').length
    }''')

    print(f'获得 {result_items_count} 条结果')

    await browser.close()

    return html_content, result_items_count

# 保存搜索结果
def save_search_result(keyword, url, html_content, result_items_count):
    search_result = GoogleSearchResult(
        search_keyword=keyword,
        search_url=url,
        search_result_html=html_content,
        result_items_count=result_items_count,
    )
    search_result.save()

# 调用搜索
async def main(keyword, url):
    connect_to_db()
    html_content, result_items_count = await get_page_html(url)
    save_search_result(keyword, url, html_content, result_items_count)

# 组织搜索 url
def search(keyword):
    print(f'开始搜索 {keyword}')
    url = f'https://www.google.com/search?q={keyword}&num=100'
    asyncio.run(main(keyword, url))

# if __name__ == '__main__':
#     search('最终幻想16')

if __name__ == '__main__':
    search_keyword = input("请输入搜索关键词: ")
    search(search_keyword)
