from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

from utils.tokens import num_tokens_from_string
from utils.print_color import prYellow

def openai_embeddings(text_list: list) -> List[List[float]]:
    """使用 openai embeddings 进行词向量化"""
    embeddings_model = OpenAIEmbeddings()
    tokens_counts = [num_tokens_from_string(text) for text in text_list]
    prYellow(tokens_counts)

    embeddings = embeddings_model.embed_documents(text_list)
    return embeddings