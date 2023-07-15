import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from logger.setup_logger import get_loguru_logger

from models.web_page_item import WebPageItem
from utils.tokens import num_tokens_from_string

def stat_tokens():
    result = {}
    for record in WebPageItem.objects:
        if record.llm_summary is None:
            continue
        result[str(record.id)] = num_tokens_from_string(record.llm_summary)

    arr = sorted(result.items(), key=lambda x: x[1], reverse=True)
    print(f'最长摘要: {arr[0]}')
    print(f'最短摘要: {arr[1]}')

def __check_text_format(text):
    # 把整段文本分成单独的行
    lines = text.split('\n')
    
    # 遍历每一行，检查是否符合格式
    for line in lines:
        # 如果行不是空行，并且也不是以"- "开头，那么返回False
        if line and not line.startswith('- '):
            return False
    
    # 如果所有的行都检查过了并且都符合格式，那么返回True
    return True

def check_summary_format():
    result = {}
    empty_count = 0
    for record in WebPageItem.objects:
        if record.llm_summary is None:
            empty_count += 1
            continue
        checked = __check_text_format(record.llm_summary)
        if not checked:
            result[str(record.id)] = checked
            print(record.id)

    print(f'无摘要记录数: {empty_count}')

if __name__ == "__main__":
    connect_to_db()
    # stat_tokens()
    check_summary_format()