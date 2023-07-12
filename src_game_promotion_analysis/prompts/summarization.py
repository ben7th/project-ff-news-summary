PROMPT_TEMPLATE_SUMMARY_FOR_PAGE = """
这是一段由爬虫抓取的文本，可能会带有广告推荐类的冗余信息：```
{content}
```

需要你帮我提取有用的句子或段落，提取时要保留原文

提取结果：
"""

def generate_summary_prompt(content):
    if not content:
        return None
    return PROMPT_TEMPLATE_SUMMARY_FOR_PAGE.format(content=content)