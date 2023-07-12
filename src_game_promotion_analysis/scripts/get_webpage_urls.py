import json
from serpapi import GoogleSearch

import os
from dotenv import load_dotenv
load_dotenv()
FREE_PLAN_SERPAPI_KEY = os.getenv('FREE_PLAN_SERPAPI_KEY')

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger.setup_logger import get_loguru_logger

import csv

def get_google_search_results(keyword):
    logger = get_loguru_logger(name='get_google_search_results', log_file_path='../logs/get_google_search_results.log')

    # 使用 SerpApi 搜索前100个结果
    params = {
        "q": keyword,
        "num": 100,
        "api_key": FREE_PLAN_SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results


if __name__ == "__main__":
    keyword_csv_path = "input/search/keywords.csv"
    time_csv_path = "input/search/dates.csv"

    # 读取关键词 CSV 文件
    with open(keyword_csv_path, "r", encoding='utf-8') as keyword_file:
        keyword_data = csv.DictReader(keyword_file)
        keyword_list = list(keyword_data)

    # 获取日志对象
    logger = get_loguru_logger(name='main', log_file_path='../logs/get_google_search_results.log', console_level='INFO')

    # 遍历关键词和时间范围执行搜索和保存结果
    for keyword_row in keyword_list:
        language = keyword_row["语言代码"]
        keyword = keyword_row["搜索词"]

        try:
            # 构建结果保存的 JSON 文件路径
            output_file_path = f"../output/search/{language}.json"
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            logger.info(f'Fetching "{keyword}" and saving to "{output_file_path}"')

            # 获取搜索结果并保存到 JSON 文件中
            search_results = get_google_search_results(keyword)
            with open(output_file_path, "w", encoding="utf-8", newline='\n') as file:
                json.dump(search_results, file, indent=2)

            # 记录搜索结果条数
            num_results = len(search_results.get("organic_results", []))
            logger.info(f'Retrieved {num_results} results for "{keyword}"')

        except Exception as e:
            logger.error(f'Error occurred while fetching search results for "{keyword}": {str(e)}')

