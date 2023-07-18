from mongoengine import Document, StringField, ListField, DictField, FloatField, IntField

class ClusteringResult(Document):
    """
    ClusteringResult 类定义了保存聚类结果的对象模型
    """
    name = StringField(required=True, unique=True)  # 聚类结果的名称，设置为唯一
    num_clusters = IntField()  # 聚类结果的簇数量
    clusters = ListField(ListField(DictField()))  # 保存所有簇的信息，每个簇是一个包含许多字典对象的数组
    clusters_texts = ListField(StringField())  # 保存所有簇对应的文本块文本信息

    meaningful_check_results = DictField()  # 内容有效性检查结果
    meaningful_texts = DictField()