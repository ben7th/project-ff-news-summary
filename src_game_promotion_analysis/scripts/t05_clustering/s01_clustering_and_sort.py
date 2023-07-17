import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('clustering_and_sort', log_file_path='../logs/clustering_and_sort.log',
                           console_level='INFO')

from dotenv import load_dotenv
load_dotenv()

from models.web_page_item import WebPageEmbeddingItem
from utils.clustering import find_best_k

def get_vector_data():
    # 从数据库中读取向量数据
    data = []
    for item in WebPageEmbeddingItem.objects():
        data.extend(item.block_embeddings)
    return data

if __name__ == "__main__":
    # 连接到 MongoDB 数据库
    connect_to_db()

    data = get_vector_data()
    # print(f'共有 {len(data)} 个向量')

    best_k_elbow, best_k_silhouette = find_best_k(data, start_k=50, end_k=300)
    print(f'best_k_elbow = {best_k_elbow}')
    print(f'best_k_silhouette = {best_k_silhouette}')

    # # # 使用最优的聚类数量进行聚类
    # # kmeans = KMeans(n_clusters=best_k, random_state=42)
    # # kmeans.fit(X)

    # # # 输出聚类结果
    # # for i, label in enumerate(kmeans.labels_):
    # #     logger.info(f"Text block {i} is assigned to cluster {label}.")