import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

import asyncio
from pyppeteer import launch

from setup.setup import connect_to_db
from models.web_page_item import WebPageItem
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger(name='extract_webpage_content', log_file_path='../logs/pyppeteer-crawler.log', 
                           log_level='ERROR', console_level='INFO')

# 连接到 MongoDB 数据库
connect_to_db()

async def get_webpage_content(url, waitUntil):
    # 启动浏览器
    browser = await launch()
    # 创建新的页面
    page = await browser.newPage()
    # 设置浏览器的 User-Agent
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

    # 导航到指定的 URL
    await page.goto(url, waitUntil=waitUntil, timeout=60000)

    # 获取网页内容
    content = await page.content()

    # 关闭浏览器
    await browser.close()

    return content


async def extract_webpage_content(url):
    try:
        content = await get_webpage_content(url, waitUntil=['load', 'domcontentloaded', 'networkidle2'])
        logger.info(f"Got content from {url}")
        return content
    except Exception as e:
        # 如果出错，将错误信息记录到日志
        logger.error(f"Failed to get content from {url} due to {e}")
        if 'Navigation Timeout Exceeded' in str(e):
            logger.info('再次尝试 waitUntil=domcontentloaded 方式')
            try:
                content = await get_webpage_content(url, waitUntil=['load', 'domcontentloaded'])
                logger.info(f"Got content from {url}")
                return content
            except Exception as e:
                logger.error(f"Failed to get content from {url} due to {e}")
                return None


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
    records = WebPageItem.objects
    count = records.count()
    for index, webpage in enumerate(records, start=1):
        if webpage.pyppeteer_content:
            continue

        logger.info(f'{index} / {count} : 抓取 {webpage.url}')
        scrape_and_save_webpage(webpage.url)

    items = WebPageItem.objects(pyppeteer_content=None)
    print('there is {} items with empty pyppeteer_content'.format(len(items)))