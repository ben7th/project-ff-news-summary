from mongoengine import Document, StringField, ListField, DictField, FloatField, IntField

class ClusteringResult(Document):
    """
    ClusteringResult 类定义了保存聚类结果的对象模型
    """
    name = StringField(required=True, unique=True)  # 聚类结果的名称，设置为唯一
    num_clusters = IntField()  # 聚类结果的簇数量
    clusters = ListField(DictField())  # 保存所有簇的信息，每个簇是一个字典