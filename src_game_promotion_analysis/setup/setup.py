# 连接到 MongoDB
from mongoengine import connect
def connect_to_db():
    connect('ff16-news-collector')