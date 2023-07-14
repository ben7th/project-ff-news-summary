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

    # goose_article = DictField()  # 使用 goose 清洗后的对象内容
    # llm_summary = StringField()  # 使用 llm 提取的原文内容

    # normalized_text_blocks = ListField()  # 按较为一致的长度（以 tokens 计算）切分后的文本片段数组
    # block_embeddings = ListField(ListField(FloatField()))  # 向量化结果
