import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.request_gpt import request_gpt
from utils.tokens import split_text_by_tokens, num_tokens_from_string
from utils.print_color import prYellow

TEMPLATE_MEANINGFUL_CHECK = '''
请判断以下内容是否为杂乱重复的无意义内容，以`是`或`否`进行回答


内容:```
{text}
```


回答:
'''

def __check_one(part):
    """检查一小段内容"""
    prompt = TEMPLATE_MEANINGFUL_CHECK.format(text=part)
    result = request_gpt(prompt)
    return result


def meaningful_check(text):
    """检测文本是否为有意义内容，返回包含 `是` `否` 的数组"""
    parts = split_text_by_tokens(text, tokens_size=1000)
    results = []
    for index, part in enumerate(parts, start=1):
        prYellow(f'request {index}/{len(parts)} tokens: {num_tokens_from_string(part)}')
        result = __check_one(part)
        results.append(result)
    return results
