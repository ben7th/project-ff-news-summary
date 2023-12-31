from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift

from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score

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


def do_clustering_kmeans(data, labels, k):
    X = np.array(data)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(X)

    # 创建一个二维列表用于存储按照聚类结果分组的标签
    clusters = [[] for _ in range(k)]
    
    # 将每个标签按照聚类结果分组
    for i, label in enumerate(labels):
        clusters[kmeans.labels_[i]].append(label)

    return clusters


def find_best_k(data, start_k=50, end_k=200):
    """
    使用肘部法则、轮廓系数、Calinski-Harabasz 指标和 Davies-Bouldin 指标寻找最佳的聚类数量

    参数:
    data: 一个包含所有向量的列表，列表中每个元素都是一个向量
    start_k: 尝试聚类数量的起始值（包含）
    end_k: 尝试聚类数量的结束值（不包含）

    返回:
    best_k_elbow: 使用肘部法则得到的最佳聚类数量
    best_k_silhouette: 使用轮廓系数得到的最佳聚类数量
    best_k_ch: 使用 Calinski-Harabasz 指标得到的最佳聚类数量
    best_k_db: 使用 Davies-Bouldin 指标得到的最佳聚类数量
    """
    # 转换数据为 numpy 数组，以便后续计算
    X = np.array(data)

    # 初始化列表，用于存储每个 k 值对应的 SSE（误差平方和）、轮廓系数、Calinski-Harabasz 指标和 Davies-Bouldin 指标
    distortions = []
    silhouette_scores = []
    calinski_harabasz_scores = []
    davies_bouldin_scores = []
    K = range(start_k, end_k)

    # 遍历所有可能的 k 值
    for k in K:
        print(f'尝试聚类 k = {k}')
        # 初始化并训练 KMeans 模型
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        kmeans.fit(X)
        # 将当前 k 值对应的 SSE 添加到列表中
        distortions.append(kmeans.inertia_)
        # 计算轮廓系数并添加到列表中
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        # 计算 Calinski-Harabasz 指标并添加到列表中
        calinski_harabasz_scores.append(calinski_harabasz_score(X, kmeans.labels_))
        # 计算 Davies-Bouldin 指标并添加到列表中
        davies_bouldin_scores.append(davies_bouldin_score(X, kmeans.labels_))

    # 计算每两个相邻 k 值的 SSE 之差，得到斜率列表
    slopes = -np.diff(distortions)
    # 找到斜率最大的点对应的 k 值，加 1 是因为 np.diff 计算的是从 start_k+1 开始的差值
    best_k_elbow = np.argmax(slopes) + start_k + 1

    # 找到轮廓系数最大的对应的 k 值
    best_k_silhouette = np.argmax(silhouette_scores) + start_k

    # 找到 Calinski-Harabasz 指标最大的对应的 k 值
    best_k_ch = np.argmax(calinski_harabasz_scores) + start_k

    # 找到 Davies-Bouldin 指标最小的对应的 k 值
    best_k_db = np.argmin(davies_bouldin_scores) + start_k

    return best_k_elbow, best_k_silhouette, best_k_ch, best_k_db


def find_peak_ks(data, start_k=50, end_k=200):
    """
    使用轮廓系数找峰值来寻找可能的最佳聚类数量

    参数:
    data: 一个包含所有向量的列表，列表中每个元素都是一个向量
    start_k: 尝试聚类数量的起始值（包含）
    end_k: 尝试聚类数量的结束值（不包含）

    返回:
    peaks: 一个列表，包含所有找到的峰值对应的聚类数量
    """
    X = np.array(data)

    silhouette_scores = []
    K = range(start_k, end_k)

    for k in K:
        print(f'尝试聚类 k = {k}')
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        kmeans.fit(X)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))

    # 计算轮廓系数的一阶差分，也就是导数
    derivatives = np.diff(silhouette_scores)

    # 初始化峰值列表
    peaks = []

    # 遍历所有导数值，找到所有从正变为负的位置，对应的就是峰值
    for i in range(1, len(derivatives)):
        if derivatives[i-1] > 0 and derivatives[i] < 0:
            peaks.append(i + start_k)

    return peaks