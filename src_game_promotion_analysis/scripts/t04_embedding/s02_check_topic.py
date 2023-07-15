import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger
logger = get_loguru_logger('check_topic', log_file_path='../logs/check_topic.log',
                           console_level='INFO')

from models.web_page_item import WebPageItem

def __fix_text(text):
    lines = text.split('\n')
    processed_lines = []
    previous_line = ''

    for line in lines:
        _line = line.strip()
        
        # 移除 "```" 行
        if _line == '```':
            continue

        # 去掉 "<" 和 ">"，只保留中间内容
        if _line.startswith('<') and _line.endswith('>'):
            _line = _line[1:-1]

        # 只保留一个空行
        if _line == '' and previous_line == '':
            continue

        processed_lines.append(_line)
        previous_line = _line

    processed_text = '\n'.join(processed_lines)
    return processed_text

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

def main():
    records = WebPageItem.objects
    total = len(records)

    errors = {}
    text_count = 0
    for index, record in enumerate(records, start=1):
        if not record.llm_topics_text:
            continue

        # print(f'{index}/{total}: {record.title} {record.id}')
        fixed_text = __fix_text(record.llm_topics_text)
        check_result = __check_text_format(fixed_text)
        text_count += 1
        # print(check_result)
        if not check_result:
            errors[str(record.id)] = record.id
            print(str(record.id))

    print(f'text_count: {text_count}')
    print(f'error_count: {len(errors)}')

if __name__ == '__main__':
    connect_to_db()
    main()