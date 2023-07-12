import json

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from llm.prompts import HTML_SUMMARY, COMMON_SUMMARY
from llm.ask_gpt import ask_gpt

from common.setup_logger import get_logger
logger = get_logger('summary', '../logs/summary-errors.log')

from mongoengine.errors import NotUniqueError

def get_summary_and_save_to_db(search_result, input_field='cleaned_html'):
    """
    获取信息摘要并保存到数据库

    :param search_result: SearchResult 对象
    :param input_field: 从 SearchResult 对象中读取的输入字段
    """
    input_text = getattr(search_result, input_field, None)
    if input_text is None:
        logger.warning(f'No {input_field} found for {search_result.url}')
        return

    try:
        # 获取信息摘要
        summary = ask_prompt_for_html(input_text)

        # 检查获取到的结果，如果是 json 格式，将其存入数据库记录的 summary_json 字段
        json.loads(summary)  # 尝试解析为 JSON，如果成功，说明它是一个有效的 JSON 字符串
        search_result.update(set__summary_json=summary, upsert=True)

    except json.JSONDecodeError as e:
        # 如果结果不能解析为 JSON，记录错误
        logger.error(f"Failed to parse summary as JSON for URL {search_result.url}: {str(e)}")
    except NotUniqueError as e:
        # 如果出现重复的 URL，记录错误日志
        logger.error(f"Duplicate URL {search_result.url}: {str(e)}")
    except Exception as e:
        # 记录其他错误日志
        logger.error(f"Error while getting summary for URL {search_result.url}: {str(e)}")


def ask_prompt_for_html(html_text: str) -> str:
    "获取 html 信息摘要"
    prompt = HTML_SUMMARY.format(html_text=html_text)
    result = ask_gpt(prompt)
    return result

def ask_prompt_for_text(text: str) -> str:
    "获取普通文本信息摘要"
    prompt = COMMON_SUMMARY.format(text=text)
    print(prompt)
    # result = ask_gpt(prompt)
    # return result