import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongoengine import connect

from utils.tokens import normalize_split_text
from utils.embedding import openai_embeddings
from models.web_page_item import WebPageItem
from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('normalize_and_embedding', log_file_path='../logs/normalize_and_embedding.log',
                           console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')


def __get_summary_text(record: WebPageItem) -> str:
    """获取摘要文本"""
    text = record.goose_article.get('cleaned_text', '')
    if text:
        return text
    
    text = record.llm_summary
    if text:
        return text
    
    return None


def __save_normalized_blocks(record: WebPageItem, summary_text: str) -> list:
    """保存归一化文本"""
    if record.normalized_text_blocks:
        return record.normalized_text_blocks

    normalized_blocks = normalize_split_text(summary_text)
    record.normalized_text_blocks = normalized_blocks
    record.save()
    logger.info(f'保存归一化文本: {record.url} {record.title}')

    return normalized_blocks


if __name__ == "__main__":
    """文本长度归一化和向量化"""

    records = WebPageItem.objects
    print(f'共 {records.count()} 条记录')

    no_summary_count = 0
    has_embeddings_count = 0
    do_embeddings_count = 0

    for record in records:
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

        print(normalized_blocks)
        embeddings = openai_embeddings(normalized_blocks)
        record.block_embeddings = embeddings
        record.save()
        logger.info(f'保存向量化结果 {len(embeddings)} blocks: {record.url} {record.title}')
        do_embeddings_count += 1

    print(f'没有摘要文本: {no_summary_count} 条记录')
    print(f'已保存过向量化结果: {has_embeddings_count} 条记录')
    print(f'保存向量化结果: {do_embeddings_count} 条记录')