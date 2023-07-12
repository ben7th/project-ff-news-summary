import json
from mongoengine import connect

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.web_page_item import WebPageItem
from logger.setup_logger import get_loguru_logger

# 获取日志对象
logger = get_loguru_logger(name='process_json_data', log_file_path='../logs/process_json_data.log')

def process_json_data(json_file_path):
    """
    从指定位置读取 json 文件，解析数据并存入 MongoDB。

    :param json_file_path: JSON 文件路径
    :type json_file_path: str
    """

    try:
        # 连接 MongoDB
        connect('ff16-news-collector')

        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历 organic_results 数组
        total_count = len(data['organic_results'])
        skipped_count = 0

        for result in data['organic_results']:
            # 提取 link 属性作为 URL
            url = result['link']

            # 使用数组对象本身作为 rawSearchResultData
            rawSearchResultData = result

            try:
                # 检查是否已存在相同的 URL 数据
                if WebPageItem.objects(url=url).first():
                    skipped_count += 1
                    logger.info(f'Skipped saving data for URL (already exists): {url}')
                    continue

                # 创建 WebPageItem 对象并保存到 MongoDB
                webpage = WebPageItem(url=url, rawSearchResultData=rawSearchResultData)
                webpage.save()
                logger.info(f'Saved data for URL: {url}')
            except Exception as e:
                logger.error(f'Error occurred while saving data for URL: {url}. Error: {str(e)}')

        logger.info(f'Data processing completed. Total items: {total_count}, Skipped items: {skipped_count}')

    except Exception as e:
        logger.error(f'Error occurred while processing JSON data. Error: {str(e)}')

if __name__ == '__main__':
    json_file_paths = [
        '../output/search/zh-cn.json',
        '../output/search/en.json',
        '../output/search/ja.json',
        '../output/search-1/zh-cn.json',
        '../output/search-1/en.json',
        '../output/search-1/ja.json',
    ]

    for json_file_path in json_file_paths:
        print('Process JSON data from: ', json_file_path)
        process_json_data(json_file_path)
