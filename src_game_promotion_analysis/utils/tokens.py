import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tiktoken
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.remove_html_tags import get_text_content

def count_tokens(text):
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    return llm.get_num_tokens(text)

def num_tokens_from_string(string: str, encoding_name: str='gpt-3.5-turbo') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text_by_tokens(text_content: str, chunk_size):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=0
    )
    texts = text_splitter.split_text(text_content)
    return texts

def normalize_text(text, max_num_tokens=500):
    lines = text.split("\n")  # 按照换行符切分文本为行

    normalized_blocks = []
    current_block = ""

    for line in lines:
        if num_tokens_from_string(current_block) + num_tokens_from_string(line) <= max_num_tokens:
            # 当前文本块长度未超过最大长度，继续添加到当前块
            current_block += line + "\n"
        else:
            # 当前文本块长度超过最大长度
            if num_tokens_from_string(line) <= max_num_tokens:
                # 新行长度小于等于最大长度，作为新的文本块
                normalized_blocks.append(current_block.strip())
                current_block = line + "\n"
            else:
                # 新行本身长度超过最大长度，单独作为一块
                normalized_blocks.append(current_block.strip())
                normalized_blocks.append(line)
                current_block = ""

    # 添加最后一个文本块
    if current_block:
        normalized_blocks.append(current_block.strip())

    return normalized_blocks