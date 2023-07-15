import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('s01_LLM_split_topic', log_file_path='../logs/s01_LLM_split_topic.log',
                           console_level='INFO')

from models.web_page_item import WebPageItem
from utils.tokens import num_tokens_from_string
from llm.llm_split_topic import llm_split_topic
from utils.print_color import prGreen

def main():
    records = WebPageItem.objects.all()
    total = len(records)

    no_llm_summary_count = 0

    for index, record in enumerate(records, start=1):
        if not record.llm_summary:
            no_llm_summary_count += 1
            continue

        if record.llm_topics_text:
            print(f'{index}/{total} - 已有 llm_topics_text 跳过')
            continue

        # 主题归纳
        tokens_num = num_tokens_from_string(record.llm_summary)
        print(f'{index}/{total} tokens: {tokens_num} - {record.title}')
        llm_topics_text = llm_split_topic(record.llm_summary)
        prGreen(llm_topics_text)
        record.llm_topics_text = llm_topics_text
        record.save()

        # break

    print(f'Total records: {total}')
    print(f'No LLM summary records: {no_llm_summary_count}')

if __name__ == '__main__':
    connect_to_db()
    main()