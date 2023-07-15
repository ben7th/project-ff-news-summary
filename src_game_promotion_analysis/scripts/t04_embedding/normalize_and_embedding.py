import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('normalize_and_embedding', log_file_path='../logs/normalize_and_embedding.log',
                           console_level='INFO')

from utils.tokens import split_text_by_tokens
from utils.embedding import openai_embeddings
from models.web_page_item import WebPageItem


def __save_normalized_blocks(record: WebPageItem, summary_text: str) -> list:
    """保存归一化文本"""
    if record.normalized_text_blocks:
        return record.normalized_text_blocks

    normalized_blocks = split_text_by_tokens(summary_text, tokens_size=300)
    record.normalized_text_blocks = normalized_blocks
    record.save()
    logger.info(f'保存归一化文本: {record.url} {record.title}')

    return normalized_blocks


def normalize_and_embedding():
    """文本长度归一化和向量化"""

    records = WebPageItem.objects
    total = records.count()
    print(f'共 {total} 条记录')

    no_summary_count = 0
    has_embeddings_count = 0
    do_embeddings_count = 0

    for index, record in enumerate(records):
        # 忽略无摘要的网页
        summary_text = __get_summary_text(record)
        if not summary_text:
            logger.info(f'没有摘要文本，忽略: {record.url} {record.title}')
            no_summary_count += 1
            continue

        # 向量化
        if record.block_embeddings:
            logger.info(f'已保存过向量化结果，忽略: {record.url} {record.title}')
            has_embeddings_count += 1
            continue

        # 保存归一化文本
        normalized_blocks = __save_normalized_blocks(record, summary_text)

        # print(normalized_blocks)
        embeddings = openai_embeddings(normalized_blocks)
        record.block_embeddings = embeddings
        record.save()
        logger.info(f'{index + 1}/{total} 保存向量化结果 {len(embeddings)} blocks: {record.url} {record.title}')
        do_embeddings_count += 1

    print(f'没有摘要文本: {no_summary_count} 条记录')
    print(f'已保存过向量化结果: {has_embeddings_count} 条记录')
    print(f'保存向量化结果: {do_embeddings_count} 条记录')

def clear():
    records = WebPageItem.objects
    count = records.count()
    for index, record in enumerate(records):
        record.normalized_text_blocks = []
        record.block_embeddings = []
        record.save()
        print(f'cleared record {index + 1}/{count}')


if __name__ == "__main__":
    # clear()
    normalize_and_embedding()