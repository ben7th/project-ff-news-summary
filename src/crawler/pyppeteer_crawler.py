import asyncio
from pyppeteer import launch
from mongoengine import connect

from models.search_result import SearchResult

import logging
from common.setup_logger import setup_logger
logger = setup_logger('../logs/pyppeteer-crawler.log', logging.ERROR)

# 连接到 MongoDB 数据库
connect('news-collector')

async def get_webpage_content(url):
    try:
        # 启动浏览器
        browser = await launch()
        # 创建新的页面
        page = await browser.newPage()
        # 导航到指定的 URL
        await page.goto(url)
        # 获取网页内容
        content = await page.content()
        # 关闭浏览器
        await browser.close()
        
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
    content = asyncio.get_event_loop().run_until_complete(get_webpage_content(url))
    # 使用 upsert 进行更新或插入操作
    SearchResult.objects(url=url).update_one(set__content=content, upsert=True)
