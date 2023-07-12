from mongoengine import connect

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.web_page_item import WebPageItem
from logger.setup_logger import get_loguru_logger

# 获取日志对象
logger = get_loguru_logger(name='process_webpage_items', log_file_path='../logs/process_webpage_items.log')

def process_webpage_items():
    """
    遍历 WebPageItem 对象，提取属性值并保存到相应字段中。
    """

    try:
        # 连接 MongoDB
        connect('ff16-news-collector')

        # 遍历 WebPageItem 对象
        for webpage in WebPageItem.objects:
            try:
                # 提取属性值
                raw_data = webpage.rawSearchResultData
                title = raw_data.get('title')
                source = raw_data.get('source')
                languages = raw_data.get('about_this_result', {}).get('languages', [])

                # 更新字段值
                webpage.title = title
                webpage.source = source
                webpage.languages = languages

                # 保存更新后的对象
                webpage.save()
                logger.info(f"Processed WebPageItem with URL: {webpage.url}")

            except Exception as e:
                logger.error(f"Error occurred while processing WebPageItem with URL: {webpage.url}. Error: {str(e)}")

        logger.info('WebPageItem processing completed.')

    except Exception as e:
        logger.error(f"Error occurred while processing WebPageItem. Error: {str(e)}")

if __name__ == '__main__':
    process_webpage_items()
