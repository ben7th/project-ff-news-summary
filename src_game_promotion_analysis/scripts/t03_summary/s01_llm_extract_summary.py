import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('llm_extract_summary', log_file_path='../logs/llm_extract_summary.log',
                           console_level='INFO')

from setup.setup import connect_to_db, disconnect_from_db
from models.web_page_item import WebPageItem
from utils.remove_html_tags import has_text_content
from llm.html_summarizer import LLM_html_summary
from utils.print_color import prGreen, prRed

def __summary(record):
    """从数据库读取内容进行摘要"""
    title = record.title
    html_text = record.pyppeteer_content

    result = LLM_html_summary(title=title, html_text=html_text, verbose=False)
    return result

def llm_extract_summary(record):
    result = __summary(record)
    prGreen(f'\n{result}')
    record.llm_summary = result
    record.save()
    prRed('已保存')

if __name__ == "__main__":
    # 连接到 MongoDB 数据库
    connect_to_db()

    """使用 LLM 生成摘要，保存到 llm_summary 字段中"""

    # [废弃] 查询 goose_article.cleaned_text 为空或为空字符串的 WebPageItem
    # [废弃] records = WebPageItem.objects(goose_article__cleaned_text__in=[None, ''])
    # 为提升效果，全部用 LLM 生成摘要，不再使用 goose_article
    records = WebPageItem.objects
    total = len(records)
    print(f'共 {total} 条待处理记录')

    passed_count = 0
    has_llm_summary_count = 0

    for index, record in enumerate(records, start=1):
        if not has_text_content(record.pyppeteer_content):
            print(f'{record.id} 记录 pyppeteer_content 无实际内容，忽略')
            passed_count += 1
            continue

        if record.llm_summary:
            print(f'{record.id} 记录 llm_summary 已存在，忽略')
            has_llm_summary_count += 1
            continue

        print(f'{index}/{total} 生成摘要')
        llm_extract_summary(record)
        # break

    print(f'共忽略 {passed_count} 条无 pyppeteer_content 内容的记录')
    print(f'共忽略 {has_llm_summary_count} 条已有 llm_summary 摘要内容的记录')