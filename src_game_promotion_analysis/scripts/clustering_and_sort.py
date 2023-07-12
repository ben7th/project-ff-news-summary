import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongoengine import connect

from utils.tokens import normalize_split_text
from utils.embedding import openai_embeddings
from models.web_page_item import WebPageItem
from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('clustering_and_sort', log_file_path='../logs/clustering_and_sort.log',
                           console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')


if __name__ == "__main__":
    """文本长度归一化和向量化"""

    records = WebPageItem.objects
    print(f'共 {records.count()} 条记录')

    no_embedding_count = 0

    all_embeddings_data = []

    for record in records:
        # 忽略无向量数据的网页
        block_embeddings = record.block_embeddings
        if not block_embeddings:
            logger.info(f'没有向量数据，忽略: {record.url} {record.title}')
            no_embedding_count += 1
            continue

        # 获取向量化数据
        all_embeddings_data.extend(block_embeddings)
    
    print(f'共 {len(all_embeddings_data)} 个向量')

    print(f'没有向量数据: {no_embedding_count} 条记录')