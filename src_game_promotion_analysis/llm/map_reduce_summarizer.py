import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tokens import split_text_by_tokens
from prompts.summarization import generate_summary_prompt_for_cluster
from llm.request_gpt import request_gpt

def map_reduce_summary(long_text):
    contents = split_text_by_tokens(long_text, chunk_size=6000)
    prompts = [generate_summary_prompt_for_cluster(content) for content in contents]

    results = []
    for prompt in prompts:
        print('request_gpt for long text summary ...')
        result = request_gpt(prompt, model='gpt-3.5-turbo-16k')
        results.append(result)

    return results