from mongoengine import Document, StringField, DateTimeField, IntField, DictField, ListField
from datetime import datetime

# MongoDB 模型
class GoogleSearchResult(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    search_url = StringField(required=True)
    search_result_html = StringField(required=True)
    result_items_count = IntField(required=True)

    result_data = ListField(DictField())