import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('add_meta', log_file_path='../logs/add_meta.log')

from models.clustering_result import ClusteringResult
from models.web_page_item import WebPageEmbeddingItem


def __merge_data(cluster_meta):
    "合并 cluster_meta 信息"
    merged_data = []
    id_mapping = {}

    for item in cluster_meta:
        id = item['id']
        line_index = item['line_index']

        if id in id_mapping:
            # 已存在相同id的项，更新line_indices
            id_mapping[id]['line_indices'].append(line_index)
        else:
            # 新的id项，创建一个新的字典项
            new_item = {'id': id, 'line_indices': [line_index]}
            id_mapping[id] = new_item
            merged_data.append(new_item)

    return merged_data

def __query_merged_meta(merged_data):
    "从 web_page_embedding_item 中检索 meta 信息"
    results = []

    for item in merged_data:
        id = item['id']
        line_indices = item['line_indices']
        embedding_item = WebPageEmbeddingItem.objects(id=id).first()
        result = {
            'embedding_item_id': id,
            'line_indices': line_indices,
            'page_meta': embedding_item.page_meta
        }
        results.append(result)

    return results
        


def main():
    cr = ClusteringResult.objects(name='ff16-kmeans-lines-2023-07-18-manual').first()

    total = len(cr.meaningful_texts)
    skipped = 0

    cr.meaningful_texts_with_meta

    for index_str, text in cr.meaningful_texts.items():
        if not text:
            print(f'skip: no text {index_str}')
            skipped += 1
            continue

        if cr.meaningful_texts_with_meta.get(index_str):
            print(f'skip: has meta data {index_str}')
            continue
        
        # 找到对应的簇信息
        cluster = cr.clusters[int(index_str)]
        merged_data = __merge_data(cluster)
        meta_data_with_url = __query_merged_meta(merged_data)
        print(meta_data_with_url)
        cr.meaningful_texts_with_meta[str(index_str)] = {
            'text': text,
            'meta_data_with_url': meta_data_with_url
        }
        cr.save()
        # break

    print(f'total: {total}')
    print(f'skipped: {skipped}')


if __name__ == "__main__":
    # 给手动筛选过的文本段落标注 meta 信息
    connect_to_db()
    main()