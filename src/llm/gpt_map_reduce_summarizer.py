import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from llm.ask_gpt import ask_gpt
from langchain.text_splitter import RecursiveCharacterTextSplitter

import logging
from common.setup_logger import get_logger
logger = get_logger(
    name='gpt-mapreduce-summary', 
    log_file_path='../logs/gpt-mapreduce-summary.log',
    console_level=logging.INFO,
)

class MapReduceProcessor:
    def __init__(self, text_splitter, map_processor, text_combiner, reduce_processor):
        self.text_splitter = text_splitter
        self.map_processor = map_processor
        self.text_combiner = text_combiner
        self.reduce_processor = reduce_processor

    def process(self, text):
        # 使用指定的文本切片方法将文本切片
        text_slices = self.text_splitter(text)

        # 创建一个空的过程数组，存放 map 后的信息
        map_texts = []

        # 遍历各个文本切片
        for index, part_text in enumerate(text_slices):
            logger.info(f'MAP: 处理文本片段 {index + 1}/{len(text_slices)}')
            # 调用指定的文本处理方法，并将处理结果收集到结果数组
            processed_text = self.map_processor(part_text)
            map_texts.append(processed_text)

        # 将结果数组传递给指定的文本组织方法，获取到一个字符串
        logger.info('COMBINE')
        combine_text = self.text_combiner(map_texts)

        # 将字符串传给指定的分析方法，获得最终结果
        if self.reduce_processor is None:
            return combine_text

        logger.info('REDUCE')
        result = self.reduce_processor(combine_text)
        return result


MAP_PROMPT = """提取以下输入文本中的信息要点，尽量保持原文，每个要点不超过 100 字

输入文本：```{text}```

按照以下格式返回提取结果：```
- 要点1
- 要点2
```
"""

REDUCE_PROMPT = """去除以下信息要点中的冗余重复条目

信息要点：```{text}```

按照以下格式返回结果```
- 要点1
- 要点2
```
"""

def split_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def get_part_summary_json(part_text):
    "请求 openapi 从文本片段获得信息摘要 JSON"
    prompt = MAP_PROMPT.format(text=part_text)
    return ask_gpt(prompt)

def combine_map_texts(map_texts):
    combine_text = "\n".join(map_texts)
    return combine_text

def reducer(text):
    prompt = REDUCE_PROMPT.format(text=text)
    return ask_gpt(prompt)

def gpt_summary(text):
    chain = MapReduceProcessor(
        text_splitter=split_text, 
        map_processor=get_part_summary_json,
        text_combiner=combine_map_texts,
        reduce_processor=reducer,
    )

    result = chain.process(text)
    return result


if __name__ == "__main__":
    from models.search_result import SearchResult
    from mongoengine import connect

    # 连接到 MongoDB 数据库
    connect('news-collector')
    item = SearchResult.objects()[0]

    print(gpt_summary(item.cleaned_html))

