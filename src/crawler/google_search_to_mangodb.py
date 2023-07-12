import requests
from serpapi import GoogleSearch
from mongoengine import connect, Document, StringField
import datetime

import logging
from common.setup_logger import setup_logger
logger = setup_logger('../logs/serpapi.log', logging.ERROR)

# 连接到 MongoDB 数据库
connect('news-collector')

class SearchResult(Document):
    """
    SearchResult 类定义了保存到 MongoDB 的对象模型
    """
    url = StringField(required=True)  # URL 字段

def save_search_results_to_db(keyword, api_key):
    """
    save_search_results_to_db 方法用于搜索指定关键词，并将搜索结果的 URL 保存到 MongoDB 数据库
    """
    # 使用 SerpApi 搜索前100个结果
    params = {
        "q": keyword,
        "num": 100,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # 从搜索结果中提取 URL
    for result in results['organic_results']:
        url = result['link']

        try:
            # 创建 SearchResult 对象并保存到数据库
            search_result = SearchResult(url=url)
            search_result.save()
        except Exception as e:
            # 如果出错，将错误信息记录到日志
            # 获取当前时间
            now = datetime.now()
            # 将当前时间转化为字符串格式
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            # 如果出错，将错误信息和当前时间记录到日志
            logger.error(f"At {timestamp}, failed to save {url} due to {e}")
