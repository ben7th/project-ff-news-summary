import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongoengine import connect

from models.web_page_item import WebPageItem
from utils.remove_html_tags import has_text_content

from prompts.summarization import generate_summary_prompt
from utils.remove_html_tags import get_text_content, remove_extra_blank_lines
from llm.request_gpt import request_gpt
from utils.tokens import num_tokens_from_string, split_text_by_tokens

from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('llm_extract_summary', log_file_path='../logs/llm_extract_summary.log',
                           console_level='INFO')

# 连接到 MongoDB 数据库
connect('ff16-news-collector')

def get_content_for_prompt(record):
    # 执行两次 get_text_content 去掉多余标签
    # 因为有的网站因为特殊的前端实现，会在 textarea 里套 html 代码
    content = get_text_content(record.pyppeteer_content)
    content = get_text_content(content)
    content = remove_extra_blank_lines(content)
    return content

def __deal_long_text_summary(record):
    """长文本，分块处理"""
    content_for_prompt = get_content_for_prompt(record)
    contents = split_text_by_tokens(content_for_prompt, chunk_size=6000)
    prompts = [generate_summary_prompt(content) for content in contents]

    results = []
    for prompt in prompts:
        print('request_gpt for long text summary ...')
        result = request_gpt(prompt, model='gpt-3.5-turbo-16k')
        results.append(result)

    return "\n".join(results)

def __summary(record):
    content_for_prompt = get_content_for_prompt(record)
    prompt = generate_summary_prompt(content_for_prompt)
    if not prompt:
        return
    
    num_tokens = num_tokens_from_string(prompt)
    logger.info(f'{num_tokens} tokens of {record.url} {record.title}')

    if num_tokens <= 8000:
        result = request_gpt(prompt, model='gpt-3.5-turbo-16k')
    else:
        # tokens > 8000 另行处理
        logger.info(f'tokens 大于 8000 {record.url} {record.title}')
        result = __deal_long_text_summary(record)

    return result


def llm_extract_summary(record):
    result = __summary(record)
    print(f'\n{result}')
    record.llm_summary = result
    record.save()

if __name__ == "__main__":
    """使用 LLM 生成摘要，保存到 llm_summary 字段中"""

    # [废弃] 查询 goose_article.cleaned_text 为空或为空字符串的 WebPageItem
    # 为提升效果，全部用 LLM 生成摘要，不再使用 goose_article
    # records = WebPageItem.objects(goose_article__cleaned_text__in=[None, ''])
    records = WebPageItem.objects()
    total = records.count()
    print(f'共 {total} 条待处理记录')

    passed_count = 0
    has_llm_summary_count = 0
    for index, record in enumerate(records, start=1):
        if not has_text_content(record.pyppeteer_content):
            print(f'{record.id} 记录 pyppeteer_content 无实际内容，忽略')
            passed_count += 1
            continue

        if record.llm_summary:
            print(f'{record.id} 记录 llm_summary 已存在，忽略')
            has_llm_summary_count += 1
            continue

        print(f'{index}/{total} 生成摘要')
        llm_extract_summary(record)

    print(f'共忽略 {passed_count} 条无 pyppeteer_content 内容的记录')
    print(f'共忽略 {has_llm_summary_count} 条已有 llm_summary 摘要内容的记录')