from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift

from sklearn.metrics import pairwise_distances
import numpy as np

def get_labels_of_cluster(clusters, cluster, labels):
    """
    获取指定簇对应的标签。

    :param clusters: 聚类结果数组，每个元素表示一个数据点所属的簇的标签或索引。
    :type clusters: list
    :param cluster: 指定簇的标签或索引。
    :type cluster: int
    :param labels: 每个数据点对应的标签数组。
    :type labels: list
    :return: 指定簇对应的标签列表。
    :rtype: list
    """
    # 创建一个空列表，用于存储指定簇对应的标签
    cluster_labels = []

    # 遍历 clusters 数组
    for i, c in enumerate(clusters):
        # 如果当前数据点的簇标签与指定簇相等
        if c == cluster:
            # 将对应数据点的标签添加到 cluster_labels 列表中
            cluster_labels.append(labels[i])

    # 返回指定簇对应的标签列表
    return cluster_labels

    # return [labels[i] for i, c in enumerate(clusters) if c == cluster]


def clustering(vectors, labels, n_clusters=100):
    """
    使用层次聚类算法进行聚类分析，按照簇的大小进行排序，返回排序后的集合

    :param vectors: 向量数组
    :type vectors: List[List[float]]
    :param labels: 字符串数组，与向量一一对应的标签
    :type labels: List[str]
    :return: 最大簇对应的标签和最接近中心的向量对应的标签
    :rtype: Tuple[List[str], str]
    """
    # 聚类分析
    # clustering = AgglomerativeClustering(n_clusters=50)
    # clustering = KMeans(n_clusters=50, n_init='auto', random_state=233)
    clustering = SpectralClustering(n_clusters=n_clusters, random_state=233)
    clusters = clustering.fit_predict(vectors)

    # 统计每个簇的大小
    cluster_sizes = np.bincount(clusters)

    # 按簇的大小进行排序
    sorted_clusters = np.argsort(cluster_sizes)[::-1]
    
    for index in range(len(sorted_clusters)):
        cluster = sorted_clusters[index]
        size = cluster_sizes[cluster]
        print(f"Cluster {cluster}: Size {size}")

    # largest_cluster = sorted_clusters[0]
    # largest_cluster_labels = get_labels_of_cluster(clusters, largest_cluster, labels)
    # print(f"Largest cluster: {largest_cluster_labels}")

    return sorted_clusters, clusters
