import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongoengine import connect

from utils.tokens import normalize_split_text
from utils.embedding import openai_embeddings
from models.web_page_item import WebPageItem
from utils.clustering import hierarchical_clustering

from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('clustering_and_sort', log_file_path='../logs/clustering_and_sort.log',
                           console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')


if __name__ == "__main__":
    """文本长度归一化和向量化"""

    records = WebPageItem.objects(languages__icontains='Chinese (China)')
    # records = WebPageItem.objects
    print(f'共 {records.count()} 条记录')

    no_embedding_count = 0

    all_embeddings_vectors = []
    all_embeddings_labels = []

    for record in records:
        # 忽略无向量数据的网页
        block_embeddings = record.block_embeddings
        if not block_embeddings:
            # logger.info(f'没有向量数据，忽略: {record.url} {record.title}')
            no_embedding_count += 1
            continue

        # 组织向量化数据和对应索引
        all_embeddings_vectors.extend(block_embeddings)
        labels = [f'{record.id}-block-{i}' for i in range(len(block_embeddings))]
        all_embeddings_labels.extend(labels)
    
    print(f'共 {len(all_embeddings_vectors)} 个向量')
    print(f'没有向量数据: {no_embedding_count} 条记录')

    # 聚类
    largest_cluster_labels = hierarchical_clustering(all_embeddings_vectors, all_embeddings_labels)
    print(largest_cluster_labels)
    print(len(largest_cluster_labels))

    # arr = label.split('-')
    # id = arr[0]
    # index = int(arr[2])

    # record = WebPageItem.objects.get(id=id)
    # block = record.normalized_text_blocks[index]
    # print(block)