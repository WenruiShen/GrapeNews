import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import datasets, linear_model

from scipy.spatial.distance import cdist, pdist
from sympy import Line,Point
import django
import logging

django.setup()
logger = logging.getLogger('dataCollector')


def draw_all_news(self, X):
    pca = PCA(n_components=2).fit(X)
    pca_result2D = pca.transform(X)
    plt.scatter(pca_result2D[:, 0], pca_result2D[:, 1], s=30, color='red')
    plt.show()

class S_C:
    def compute_K(self, X):
        dict1 = {}
        min_K_num = 2
        max_K_num = max(2, min(10, int(X.shape[0])) )
        #max_K_num = max(2, int(X.shape[0]))
        K_num_step = 1 if max_K_num <= 10 else 2
        #draw_all_news(X)
        for n_cluster in range(min_K_num, max_K_num, K_num_step):
            if X.shape[0] < n_cluster:
                break
            kmeans = KMeans(n_clusters=n_cluster).fit(X)
            label = kmeans.labels_
            sil_coeff = silhouette_score(X, label, metric='euclidean')
            dict1[n_cluster]=sil_coeff
            #logger.debug("For n_clusters={}, The Silhouette Coefficient is {}".format(n_cluster, sil_coeff))
        return dict1

    def compute_K_elbow(self, X):
        dict1 = {}
        pca = PCA(n_components=2).fit(X)
        X = pca.transform(X)

        min_K_num = 2
        max_K_num = max(2, min(10, int(X.shape[0])))
        K_num_step = 1 if max_K_num <= 10 else 2
        K_num_list = [k for k in range(min_K_num, max_K_num, K_num_step)]

        kMeansVar = [KMeans(n_clusters=k).fit(X) for k in K_num_list]
        centroids = [X.cluster_centers_ for X in kMeansVar]
        k_euclid = [cdist(X, cent) for cent in centroids]
        dist = [np.min(ke, axis=1) for ke in k_euclid]
        wcss = [sum(d ** 2) for d in dist]
        tss = sum(pdist(X) ** 2) / X.shape[0]
        bss = tss - wcss

        index = 0
        for elbow_value in bss:
            K_num = K_num_list[index]
            dict1[K_num] = elbow_value
            index = index + 1
        return dict1

    def elbow_mean_distortion(self, R2D):
        try:
            dict1 = {}

            pca = PCA(n_components=2).fit(R2D)
            R2D = pca.transform(R2D)

            K_list = range(2, R2D.shape[0])
            for k in K_list:
                kmeans = KMeans(n_clusters=k)
                kmeans.fit(R2D)
                meandistortions = sum(np.min(cdist(R2D, kmeans.cluster_centers_, 'euclidean'), axis=1)) / R2D.shape[0]
                dict1[k] = meandistortions
            return dict1
        except:
            return None

    def Choose_cluster_number(sc_dis):
        list_1 = sorted(sc_dis.items(), key=lambda item: item[1], reverse=True)
        h_sc = list_1[0]
        cluster_number = h_sc[0]
        higher_score = h_sc[1]
        return cluster_number

    def Choose_cluster_number_smallest(sc_dis):
        list_1 = sorted(sc_dis.items(), key=lambda item: item[1], reverse=False)
        h_sc = list_1[0]
        cluster_number = h_sc[0]
        higher_score = h_sc[1]
        return cluster_number

    def Choose_cluster_number_distance(self, dict1):
        list_2 = sorted(dict1.items(), key=lambda item: item[0])
        point1 = Point(list_2[0])
        point2 = Point(list_2[-1])
        line = Line(point1, point2)
        Q = 1
        dis = {}
        for p in list_2:
            P = Point(p)
            D = line.distance(P)
            dis[Q] = D
            Q = Q + 1
        list_1 = sorted(dis.items(), key=lambda item: item[1], reverse=True)
        h_sc = list_1[0]
        cluster_number = h_sc[0]
        # higher_score = h_sc[1]
        logger.info("Best K value is" + str(cluster_number))
        return cluster_number

    def silh_coef_and_cluster_num_linear_regression(self, k_num_silh_coef_dict):
        if k_num_silh_coef_dict is None:
            return None
        k_num_silh_coef_list = sorted(k_num_silh_coef_dict.items(), key=lambda item: item[0], reverse=False)
        cluster_num_list_X = []
        for silh_coef in k_num_silh_coef_list:
            cluster_num_list_X.append([silh_coef[0]])
        silh_coef_list_Y = [silh_coef[1] for silh_coef in k_num_silh_coef_list]

        # Linear regression.
        regr = linear_model.LinearRegression()
        regr.fit(cluster_num_list_X, silh_coef_list_Y)

        cluster_num_diff_dict = {}
        for cluster_num in cluster_num_list_X:
            predict_outcome = regr.predict(cluster_num[0])
            predictions = {}
            predictions['predicted_value'] = predict_outcome[0]
            predictions['silh_coef_diff'] = k_num_silh_coef_dict[cluster_num[0]] - predictions['predicted_value']
            cluster_num_diff_dict[cluster_num[0]] = predictions['silh_coef_diff']
            logger.debug("cluster_num: " + str(cluster_num[0]) + \
                        "; actual_value: " + str(k_num_silh_coef_dict[cluster_num[0]]) + \
                        "; predicted_value: " + str(predictions['predicted_value']) + \
                        "; silh_coef_diff: " + str(predictions['silh_coef_diff']))

        # Get the elbow point.
        cluster_number = S_C.Choose_cluster_number(cluster_num_diff_dict)
        #cluster_number = S_C.Choose_cluster_number_smallest(cluster_num_diff_dict)
        '''
        plt.plot(cluster_num_list_X, silh_coef_list_Y, color='blue', linewidth=4)
        plt.plot(cluster_num_list_X, regr.predict(cluster_num_list_X), color='red', linewidth=4)
        plt.scatter([cluster_number], [k_num_silh_coef_dict[cluster_number]], marker = 'x', s = 60, linewidths = 6, color = 'orange')
        plt.show()
        '''
        return cluster_number



