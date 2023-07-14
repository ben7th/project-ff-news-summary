from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

# MongoDB 模型
class GoogleSearchResult(Document):
    search_url = StringField(required=True)
    search_result_html = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)