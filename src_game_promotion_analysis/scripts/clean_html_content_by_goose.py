import os
from goose3 import Goose
from goose3.text import StopWordsChinese
from goose3.crawler import CrawlCandidate
from mongoengine import connect
import traceback

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.web_page_item import WebPageItem

from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger(name='clean_html_by_goose', log_file_path='../logs/clean_html_by_goose.log', log_level='ERROR')

from utils.remove_html_tags import remove_html_script_tags

# 连接到 MongoDB 数据库
connect('ff16-news-collector')

def __get_g_from_language(language) -> Goose:
    if language is None:
        return Goose()
    elif "chinese" in language.lower():
        return Goose({'stopwords_class': StopWordsChinese})
    elif "japanese" in language.lower():
        return Goose()
    else:
        return Goose()


def clean_html(html_content, language=None, origin_url=None) -> dict:
    """
    使用 goose 清洗 HTML 内容，返回 article 对象。

    :param html_content: HTML 内容
    :type html_content: str
    :return: 清洗后的 article 对象
    :rtype: dict
    """
    g = __get_g_from_language(language)

    # 清除不必要的 script 标签，避免 meta 解析的错误
    html_content_without_script_tags = remove_html_script_tags(html_content)

    # hack 方法, 传入 url, 避免 `'list' object has no attribute 'decode'` 错误
    crawl_candidate = CrawlCandidate(g.config, url=origin_url, raw_html=html_content_without_script_tags)
    # hack 方法，调用私有方法
    article = g._Goose__crawl(crawl_candidate)
    return article.infos

def clean_and_save_html_content():
    """
    从数据库中获取还未清洗的记录，清洗并保存 article 对象信息。
    """
    records = WebPageItem.objects
    total_count = records.count()
    cleaned_count = 0

    for record in records:
        # 检查是否已经清洗过内容
        cleaned_text = record.goose_article.get('cleaned_text', '')

        if cleaned_text:
            continue

        # 获取 pyppeteer_content 字段的内容
        html_content = record.pyppeteer_content
        if not html_content:
            continue

        languages = record.languages
        if len(languages) > 1:
            logger.error(f'语言信息多于一种 {record.id}: {languages}')
            continue

        language = languages[0] if len(languages) == 1 else None
        origin_url = record.url
        # print(origin_url)

        try:
            # 清洗 HTML 内容
            cleaned_article = clean_html(html_content, language=language, origin_url=origin_url)

            # 将清洗后的内容保存到数据库
            record.goose_article = cleaned_article
            record.save()
            cleaned_count += 1

            print(f"Saved cleaned HTML content to {record.id}")
        except Exception as e:
            logger.error(f'Failed to clean HTML content of record {record.id}: {e}')
            print(traceback.format_exc())

    print(f'Cleaned {cleaned_count}/{total_count} records')


def stat():
    records = WebPageItem.objects
    total_count = records.count()
    with_goose_article_count = 0
    with_goose_cleaned_text_count = 0

    for record in records:
        if record.goose_article:
            with_goose_article_count += 1
            cleaned_text = record.goose_article.get('cleaned_text', '')
            if cleaned_text:
                with_goose_cleaned_text_count += 1

    print(f'总数量 : {total_count}')
    print(f'已正确由 goose 处理的数量 ： {with_goose_article_count}')
    print(f'已获取由 goose 清洗后的文本 ： {with_goose_cleaned_text_count}')

if __name__ == "__main__":
    clean_and_save_html_content()
    stat()