import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('meaningful_check', log_file_path='../logs/meaningful_check.log')

from models.clustering_result import ClusteringResult
from llm.meaningful_check import meaningful_check
from utils.tokens import split_text_by_tokens

def __meaningful_check():
    cr = ClusteringResult.objects(name='ff16-kmeans-lines-2023-07-18').first()
    total = len(cr.clusters_texts)

    meaningful_check_results = cr.meaningful_check_results

    for index, text in enumerate(cr.clusters_texts, start=0):
        if meaningful_check_results[str(index)]:
            print(f'skip {index+1}/{total}')
            continue

        print(f'meaningful_check {index+1}/{total}')
        results = meaningful_check(text)
        print(results)
        meaningful_check_results[str(index)] = results
        cr.meaningful_check_results = meaningful_check_results
        cr.save()

def __parse_text(parts, check_result):
    results = []
    for i in range(len(parts)):
        useful = check_result[i] == '否'
        if useful:
            results.append(parts[i])

    return "\n".join(results)

def __save_meaningful_text():
    cr = ClusteringResult.objects(name='ff16-kmeans-lines-2023-07-18').first()

    total = len(cr.meaningful_check_results.items())
    meaningful_check_results = cr.meaningful_check_results
    
    for index, text in enumerate(cr.clusters_texts, start=0):
        print(f'meaningful_check {index+1}/{total}')
        parts = split_text_by_tokens(text, tokens_size=1000)
        check_result = meaningful_check_results[str(index)]
        meaningful_text = __parse_text(parts, check_result)
        cr.meaningful_texts[str(index)] = meaningful_text
        cr.save()
        # break

if __name__ == '__main__':
    connect_to_db()
    # __meaningful_check()
    __save_meaningful_text()