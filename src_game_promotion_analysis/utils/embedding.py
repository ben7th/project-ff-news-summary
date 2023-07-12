from typing import List
from langchain.embeddings.openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

def openai_embeddings(text_list: list) -> List[List[float]]:
    """使用 openai embeddings 进行词向量化"""
    embeddings_model = OpenAIEmbeddings()
    embeddings = embeddings_model.embed_documents(text_list)
    return embeddings