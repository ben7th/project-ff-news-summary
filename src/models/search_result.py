from mongoengine import Document, StringField

class SearchResult(Document):
    """
    SearchResult 类定义了保存到 MongoDB 的对象模型
    """
    url = StringField(required=True, unique=True)  # URL 字段，设置为唯一
    content = StringField()  # 网页内容

    cleaned_html = StringField()  # 清理后的网页内容
    cleaned_text = StringField()  # 清理后的文本，去掉所有 html 标签

    summary_json = StringField()  # JSON 摘要
    summary_text = StringField()  # 文本摘要