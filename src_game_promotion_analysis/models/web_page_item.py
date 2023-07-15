from mongoengine import Document, StringField, DictField, ListField, FloatField

class WebPageItem(Document):
    """
    WebPageItem 类定义了保存到 MongoDB 的对象模型
    """
    url = StringField(required=True, unique=True)  # URL 字段，设置为唯一
    title = StringField()  # 从搜索结果中信息获取的网页标题
    source = StringField()  # 从搜索结果信息中获取的网页来源
    language = StringField()  # 从搜索结果中信息获取的网页语言

    pyppeteer_content = StringField()  # 使用 pyppeteer 抓取的网页 html 内容

    llm_summary = StringField()  # 使用 LLM 提取的原文要点内容
    llm_topics_text = StringField()  # 使用 LLM 划分主题后的要点内容


class WebPageEmbeddingItem(Document):
    """保存向量化信息"""

    url = StringField(required=True, unique=True)  # URL 字段，设置为唯一
    page_meta = DictField(required=True)  # url, title, source, language

    normalized_text_blocks = ListField()  # 按 <主题要点文本> fix 并切分后的文本块