from common.setup_logger import get_logger
logger = get_logger('summary', '../logs/TextSummarizer.log')

import json
from mongoengine.errors import NotUniqueError

class TextSummarizer:
    def __init__(self, summarizer):
        self.summarizer = summarizer

    def summarize_and_save(self, mongo_object, input_field, output_field):
        """
        从指定对象的字段读取信息，进行文本摘要，并将结果更新到指定的字段上

        :param object: 输入的对象
        :param input_field: 从该对象中读取的输入字段
        :param output_field: 将结果更新到该对象的指定字段
        """
        # 从指定字段读取输入
        input_text = getattr(mongo_object, input_field, None)
        if input_text is None:
            logger.warning(f'No {input_field} found for the object.')
            return

        try:
            # 获取信息摘要
            summary_text = self.summarizer(input_text)
            mongo_object.update(**{f'set__{output_field}': summary_text})

        except NotUniqueError as e:
            # 如果出现重复的字段值，记录错误日志
            logger.error(f"Duplicate field value {input_field}: {str(e)}")

        except Exception as e:
            # 记录其他错误日志
            print(e)
            logger.error(f"Error while summarizing: {str(e)}")

from llm.gpt_map_reduce_summarizer import gpt_summary
record_summarizer = TextSummarizer(summarizer=gpt_summary)