# 连接到 MongoDB
from mongoengine import connect, disconnect
def connect_to_db():
    connect('ff16-news-collector')

def disconnect_from_db():
    disconnect()