import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('clustering_summary', log_file_path='../logs/clustering_summary.log',
                           console_level='INFO')

from models.clustering_result import ClusteringResult
from models.web_page_item import WebPageEmbeddingItem

def get_text_block_of_cluster(id_idx_item):
    # { id, block_index }
    # print(id_idx_item)
    id = id_idx_item.get('id')
    block_index = id_idx_item.get('block_index')
    return WebPageEmbeddingItem.objects(id=id).first().normalized_text_blocks[block_index]

def main():
    cr = ClusteringResult.objects(name='ff16-kmeans-2023-07-18').first()

    clusters_texts = []
    for cindex, cluster in enumerate(cr.clusters):
        cluster_text_block = []
        for item in cluster:
            # { id, block_index }
            text_block = get_text_block_of_cluster(item)
            cluster_text_block.append(text_block)
        cluster_text = '\n\n'.join(cluster_text_block)
        print(f'cindex: {cindex}')
        print(cluster_text)
        print()

        clusters_texts.append(cluster_text)

    cr.clusters_texts = clusters_texts
    cr.save()
    print(f'结果已保存')

if __name__ == '__main__':
    connect_to_db()
    main()