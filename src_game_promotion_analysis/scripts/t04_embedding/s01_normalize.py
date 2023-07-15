import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('normalize_and_embedding', log_file_path='../logs/normalize_and_embedding.log',
                           console_level='INFO')

from utils.tokens import normailze_text_for_llm_summary
from models.web_page_item import WebPageItem


def __save_normalized_blocks(record: WebPageItem, summary_text: str) -> list:
    """保存归一化文本"""
    normalized_blocks = normailze_text_for_llm_summary(summary_text, chunk_size=300)

    # # 保存到数据库
    # record.normalized_text_blocks = normalized_blocks
    # record.save()
    # logger.info(f'保存归一化文本: {record.url} {record.title}')

    return normalized_blocks


def normalize():
    """文本长度归一化"""

    records = WebPageItem.objects
    total = len(records)
    print(f'共 {total} 条记录')

    no_summary_count = 0

    for index, record in enumerate(records):
        summary_text = record.llm_summary

        # 保存归一化文本
        normalized_blocks = __save_normalized_blocks(record, summary_text)
        for block in normalized_blocks:
            print(block)
            print("---\n")

        break

    print(f'共忽略没有摘要文本的 {no_summary_count} 条记录')

if __name__ == "__main__":
    connect_to_db()
    normalize()