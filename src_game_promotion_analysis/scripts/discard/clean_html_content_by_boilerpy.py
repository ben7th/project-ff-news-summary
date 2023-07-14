import os
from mongoengine import connect
from boilerpy3 import extractors

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.web_page_item import WebPageItem

from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger(name='clean_html_by_boilerpy', log_file_path='../logs/clean_html_by_boilerpy.log', log_level='ERROR')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')

def clean_html(html_content, language):
    extractor = extractors.ArticleExtractor()
    doc = extractor.get_doc(html_content)
    print(extractor.get_marked_html(html_content))
    return doc

def clean_and_save_html_content():
    """
    从数据库中获取还未清洗的记录，清洗并保存 article 对象信息。
    """
    records = WebPageItem.objects[:1]
    total_count = records.count()
    cleaned_count = 0

    for record in records:
        # 检查是否已经清洗过内容
        # cleaned_text = record.goose_article.get('cleaned_text', '')

        # if cleaned_text:
        #     continue

        # 获取 pyppeteer_content 字段的内容
        html_content = record.pyppeteer_content
        if not html_content:
            continue

        languages = record.languages
        if len(languages) != 1:
            logger.error(f'无法正确获取语言信息 {record.id}: {languages}')
            continue

        language = languages[0]

        cleaned_article = clean_html(html_content, language=language)
        print(cleaned_article.title)
        print(cleaned_article.content)
        print(cleaned_article.text_blocks)

        # try:
        #     # 清洗 HTML 内容
        #     cleaned_article = clean_html(html_content, language=language)

        #     # 将清洗后的内容保存到数据库
        #     record.goose_article = cleaned_article
        #     record.save()
        #     cleaned_count += 1

        #     print(f"Saved cleaned HTML content to {record.id}")
        # except Exception as e:
        #     logger.error(f'Failed to clean HTML content of record {record.id}: {str(e)}')
        #     # logger.error(traceback.format_exc())

    print(f'Cleaned {cleaned_count}/{total_count} records')

if __name__ == "__main__":
    clean_and_save_html_content()
