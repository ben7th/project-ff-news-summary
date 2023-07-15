import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.request_gpt import request_gpt
from utils.tokens import num_tokens_from_string, split_text_by_tokens
from utils.print_color import prYellow

prompt_template = """请对以下要点列表按照主题进行划分:


```{text}```


请按以下格式输出:```
<主题>
- <要点>
```


划分结果:"""

def __LLM_split_by_topic(text, index):
    prompt = prompt_template.format(text=text)
    # print(prompt)
    prYellow(f'request {index} ... tokens: {num_tokens_from_string(prompt)}')
    result = request_gpt(prompt)
    return result

def llm_split_topic(long_text):
    results = []
    prYellow(f'text tokens: {num_tokens_from_string(long_text)}')
    splitted_texts = split_text_by_tokens(long_text, 1500)
    for index, text in enumerate(splitted_texts, start=1):
        result = __LLM_split_by_topic(text, index)
        results.append(result)
    
    return "\n\n".join(results)