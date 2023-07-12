import asyncio
from pyppeteer import launch
from mongoengine import connect

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.web_page_item import WebPageItem

from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger(name='extract_webpage_content', log_file_path='../logs/pyppeteer-crawler.log', 
                           log_level='ERROR', console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')

async def extract_webpage_content(url):
    try:
        # 启动浏览器
        browser = await launch()
        # 创建新的页面
        page = await browser.newPage()

        # 导航到指定的 URL
        await page.goto(url, waitUntil='load', timeout=60000)

        # 获取网页内容
        content = await page.content()

        # 关闭浏览器
        await browser.close()

        logger.info(f"Got content from {url}")

        return content
    except Exception as e:
        # 如果出错，将错误信息记录到日志
        logger.error(f"Failed to get content from {url} due to {e}")


def scrape_and_save_webpage(url):
    """
    获取指定 URL 的网页内容，并将其保存到 MongoDB 数据库。
    如果数据库中已存在相同 URL 的记录，则更新该记录；否则，创建新的记录。
    :param url: 需要获取内容的网页的 URL
    """
    # 运行 get_webpage_content 函数
    content = asyncio.get_event_loop().run_until_complete(extract_webpage_content(url))
    # 使用 upsert 进行更新或插入操作
    if content is not None:
        WebPageItem.objects(url=url).update_one(set__pyppeteer_content=content, upsert=True)

if __name__ == '__main__':
    for webpage in WebPageItem.objects:
        if webpage.pyppeteer_content is None:
            scrape_and_save_webpage(webpage.url)

    # items = WebPageItem.objects(pyppeteer_content=None)
    # print('there is {} items with empty pyppeteer_content'.format(len(items)))