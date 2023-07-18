import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('split_by_line', log_file_path='../logs/split_by_line.log',
                           console_level='INFO')

from models.web_page_item import WebPageItem, WebPageEmbeddingItem
from utils.texts import fix_text

def __split_lines(input_text):
    lines = input_text.split('\n')  # 按行切分文本
    result = [line.strip() for line in lines if line.strip()]  # 保存非空行，并对每行进行strip操作
    return result

def save_lines_to_db(record, lines):
    url = record.url

    WebPageEmbeddingItem.objects(url=url).update_one(
        set__normalized_text_lines=lines,
        upsert=True
    )

    return len(lines)

def main():
    # 读取数据
    records = WebPageItem.objects
    total = len(records)

    text_count = 0
    parts_count = 0

    for index, record in enumerate(records, start=1):
        # 跳过没有 llm_topics_text (LLM 主题摘要文本) 的记录
        if not record.llm_topics_text:
            print(f'skipping {index}/{total}')
            continue
        
        fixed_topics_text = fix_text(record.llm_topics_text)
        lines = __split_lines(fixed_topics_text)

        text_count += 1
        parts_count += save_lines_to_db(record, lines)

    print(f'总摘要文本数量: {text_count}')
    print(f'总片段数量: {parts_count}')

if __name__ == '__main__':
    connect_to_db()
    main()