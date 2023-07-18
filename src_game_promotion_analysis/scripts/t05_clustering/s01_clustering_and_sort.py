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
from utils.clustering import find_peak_ks
from utils.clustering import do_clustering_kmeans

def get_vector_data():
    # 从数据库中读取向量数据
    data = []
    labels = []
    for item in WebPageEmbeddingItem.objects:
        data.extend(item.block_embeddings)
        for index, _ in enumerate(item.block_embeddings):
            label = {'id': str(item.id), 'block_index': index}
            labels.append(label)
    return data, labels

def __find_best_k(data):
    best_k_elbow, best_k_silhouette, best_k_ch, best_k_db = find_best_k(data, start_k=50, end_k=200)
    print(f'best_k_elbow = {best_k_elbow}')
    print(f'best_k_silhouette = {best_k_silhouette}')
    print(f'best_k_ch = {best_k_ch}')
    print(f'best_k_db = {best_k_db}')

    # peaks = find_peak_ks(data)
    # print(f'peaks: {peaks}')


if __name__ == "__main__":
    # 连接到 MongoDB 数据库
    connect_to_db()

    # 获取数据
    data, labels = get_vector_data()
    print(f'共有 {len(data)} 个向量')
    
    # 找出最佳 k 值
    # __find_best_k(data)

    # best_k_elbow = 71
    # best_k_silhouette = 198
    # best_k_ch = 50
    # best_k_db = 199

    # 使用最优的聚类数量进行聚类
    best_k = 71
    clusters = do_clustering_kmeans(data, labels, k=best_k)

    # 输出聚类结果
    # for i, label in enumerate(kmeans.labels_):
    #     logger.info(f"Text block {i} is assigned to cluster {label}.")
    clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
    for idx, c in enumerate(clusters):
        print(f'index: {idx}, len: {len(c)}')
        print(c)
        print()