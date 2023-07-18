import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('check_topic', log_file_path='../logs/check_topic.log',
                           console_level='INFO')

from models.web_page_item import WebPageItem, WebPageEmbeddingItem
from utils.texts import fix_text

def __check_text_format(text):
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        
        # 检查标题行
        if len(lines) < 2 or lines[0].startswith('- '):
            return False
        
        # 检查要点行
        for line in lines[1:]:
            if not line.startswith('- '):
                return False
    
    return True

def __save_embedding_item(record, fixed_topics_text):
    url = record.url
    page_meta = {
        'url': record.url,
        'title': record.title,
        'source': record.source,
        'language': record.language
    }
    normalized_text_blocks = fixed_topics_text.split('\n\n')

    WebPageEmbeddingItem.objects(url=url).update_one(
        set__page_meta=page_meta,
        set__normalized_text_blocks=normalized_text_blocks,
        upsert=True
    )

    return len(normalized_text_blocks)

def main():
    records = WebPageItem.objects
    total = len(records)

    errors = {}
    text_count = 0
    parts_count = 0

    for index, record in enumerate(records, start=1):
        if not record.llm_topics_text:
            continue

        # print(f'{index}/{total}: {record.title} {record.id}')
        fixed_topics_text = fix_text(record.llm_topics_text)
        check_result = __check_text_format(fixed_topics_text)
        text_count += 1

        parts_count += __save_embedding_item(record, fixed_topics_text)

        # print(check_result)
        if not check_result:
            errors[str(record.id)] = record.id
            print(str(record.id))

    print(f'text_count: {text_count}')
    print(f'error_count: {len(errors)}')
    print(f'总片段数量: {parts_count}')

if __name__ == '__main__':
    connect_to_db()
    main()