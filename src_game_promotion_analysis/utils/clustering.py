from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
import numpy as np

def hierarchical_clustering(vectors, labels):
    """
    使用层次聚类算法进行聚类分析，找到最大簇对应的标签和最接近中心的向量对应的标签。

    :param vectors: 向量数组
    :type vectors: List[List[float]]
    :param labels: 字符串数组，与向量一一对应的标签
    :type labels: List[str]
    :return: 最大簇对应的标签和最接近中心的向量对应的标签
    :rtype: Tuple[List[str], str]
    """
    # 聚类分析
    clustering = AgglomerativeClustering(metric='euclidean', linkage='ward', n_clusters=100)
    clusters = clustering.fit_predict(vectors)

    # 找到最大的簇
    cluster_sizes = np.bincount(clusters)
    largest_cluster_index = np.argmax(cluster_sizes)

    print(cluster_sizes)

    # 获取最大簇的标签
    largest_cluster_labels = [labels[i] for i, cluster in enumerate(clusters) if cluster == largest_cluster_index]

    # 找到最大簇的中心向量
    largest_cluster_vectors = [vectors[i] for i, cluster in enumerate(clusters) if cluster == largest_cluster_index]
    largest_cluster_center = np.mean(largest_cluster_vectors, axis=0)

    # 找到最接近中心的向量索引
    distances = pairwise_distances(vectors, [largest_cluster_center], metric='euclidean')
    closest_vector_index = np.argmin(distances)

    # 获取最接近中心的向量对应的标签
    closest_vector_label = labels[closest_vector_index]

    return largest_cluster_labels, closest_vector_label
