import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongoengine import connect

from utils.tokens import normalize_split_text
from utils.embedding import openai_embeddings
from models.web_page_item import WebPageItem
from utils.clustering import clustering, get_labels_of_cluster
from llm.map_reduce_summarizer import map_reduce_summary

from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('clustering_and_sort', log_file_path='../logs/clustering_and_sort.log',
                           console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')

def get_text_blocks_of_labels(labels):
    blocks = []

    for label in labels:
        [id, _, index] = label.split('-')
        record = WebPageItem.objects(id=id).first()
        text_block = record.normalized_text_blocks[int(index)]
        blocks.append(text_block)

    return blocks

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
    sorted_clusters, clusters = clustering(all_embeddings_vectors, all_embeddings_labels, n_clusters=50)
    
    # 最大的簇
    largest_cluster = sorted_clusters[0]
    largest_cluster_labels = get_labels_of_cluster(clusters, largest_cluster, all_embeddings_labels)
    # print(f"Largest cluster: {largest_cluster_labels}")
    # ids = [label.split('-')[0] for label in largest_cluster_labels]
    # unique_ids = list(set(ids))
    # print(f"IDs: {unique_ids}")

    # cluster_records = WebPageItem.objects(id__in=unique_ids)
    # print([record.title for record in cluster_records])

    blocks = get_text_blocks_of_labels(largest_cluster_labels)
    print(blocks)
    cluster_text = '\n'.join(blocks)
    result = map_reduce_summary(cluster_text)
    print(result)

