from dotenv import load_dotenv
load_dotenv()

import os
import json
import inquirer
from mongoengine import connect

from crawler.google_search_to_mangodb import save_search_results_to_db
from common.clean_html import remove_tags_and_save_to_db
from common.clean_html import remove_tags_and_save_text_to_db
from crawler.pyppeteer_crawler import scrape_and_save_webpage

from models.search_result import SearchResult

# 连接到 MongoDB 数据库
connect('news-collector')

FREE_PLAN_SERPAPI_KEY = os.getenv('FREE_PLAN_SERPAPI_KEY')

OUTPUT_FILE_PATH = '../output/output.json'

def collect_search_results():
    search_term = '吉田 FF16 最终幻想16'
    save_search_results_to_db(
        keyword=search_term,
        api_key=FREE_PLAN_SERPAPI_KEY
    )


def collect_by_pyppeteer():
    """
    遍历 MongoDB 数据库中的 SearchResult 记录，根据每条记录的 URL 调用 scrape_and_save_webpage 函数抓取网页
    """
    # 从 MongoDB 数据库中获取所有 SearchResult 记录

    search_results = SearchResult.objects.all()

    print(f'需要抓取 {len(search_results)} 条记录 ...')
    # 遍历所有记录
    for index, search_result in enumerate(search_results):
        # 获取记录的 URL
        url = search_result.url
        print(f'{index} - 抓取 {url} ...')
        # 调用 scrape_and_save_webpage 函数抓取网页并保存
        scrape_and_save_webpage(url)


def clean_html():
    """
    从数据库读取 SearchResult 对象，清理 HTML 并保存到数据库
    """
    # 获取 SearchResult 的所有对象
    all_search_results = SearchResult.objects()
    
    # 遍历所有 SearchResult 对象
    for index, search_result in enumerate(all_search_results):
        # 对每一个 SearchResult 对象，去除 HTML 中的特定标签并保存到数据库
        # 获取记录的 URL
        url = search_result.url
        print(f'{index} - 清洗 {url} ...')
        remove_tags_and_save_to_db(search_result)


def clean_html_to_text():
    """
    从数据库读取 SearchResult 对象，清理 HTML 并保存到数据库
    """
    # 获取 SearchResult 的所有对象
    all_search_results = SearchResult.objects()
    
    # 遍历所有 SearchResult 对象
    for index, search_result in enumerate(all_search_results):
        # 对每一个 SearchResult 对象，去除 HTML 中的特定标签并保存到数据库
        # 获取记录的 URL
        url = search_result.url
        print(f'{index} - 清洗 {url} ...')
        remove_tags_and_save_text_to_db(search_result)


def get_all_summary():
    """
    遍历数据库中所有数据，逐个获取信息摘要并保存
    """
    # 使用 SearchResult.objects() 获取数据库中的所有数据
    search_results = SearchResult.objects()

    total = len(search_results)  # 获取总数
    input_field = 'cleaned_html'
    output_field = 'summary_text'
    print(f'记录总数: {total}')
    print(f'摘要输入字段: {input_field}')
    print(f'摘要输出字段: {output_field}')

    from llm.text_summarizer import record_summarizer

    # 遍历数据
    for index, search_result in enumerate(search_results, start=1):  # 添加一个从1开始的计数器
        # 打印进度信息
        print(f'[{index}/{total}] 正在生成摘要 {search_result.url} ...')

        # 保存摘要
        record_summarizer.summarize_and_save(
            search_result, 
            input_field=input_field,
            output_field=output_field
        )


def cli():
    # 存储方法的字典
    methods = {
        'collect_search_results': collect_search_results, # 抓取网址
        'collect_by_pyppeteer': collect_by_pyppeteer, # 抓取内容
        'clean_html': clean_html, # 清理网页
        'clean_html_to_text': clean_html_to_text, # 清理网页，仅保留文本
        'get_all_summary': get_all_summary # 获取信息摘要
    }

    # 定义选项列表
    options = [
        inquirer.List('method',
                    message="请选择一个方法来运行",
                    choices=list(methods.keys()),
                    ),
    ]

    # 获取用户选择
    answers = inquirer.prompt(options)
    # 根据用户选择运行相应的方法
    selected_method = methods.get(answers['method'])
    if selected_method:
        selected_method()
    else:
        print("无效的选择")

if __name__ == '__main__':
    cli()