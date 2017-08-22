import io
import os
import sys
import codecs
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import KMeans
#import heapq
import operator
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances_argmin_min

from dataCollector.Silhouette_Coefficient import S_C
import dataCollector.Remove_outlier
import django
import logging

logger = logging.getLogger('dataCollector')

def f_get_sorted_index_array(terms_weight_sum_array, select_num):
    return np.argsort(terms_weight_sum_array)[::-1][:select_num]

def drop_useless_words(charact_words_dictionary):
    useless_words_list = ["said", "wa", "ha", "mr", "fa", "cnn", "bbc"]
    for useless_word in useless_words_list:
        if useless_word in charact_words_dictionary.keys():
            del charact_words_dictionary[useless_word]
    return charact_words_dictionary


#******************************************************************************************
#    Function description: Main body of K-means clustering.                               *
#******************************************************************************************
def f_k_meanCluster(data_ndarray, K):
    # find 4 clusters
    R_O = dataCollector.Remove_outlier.R_outlier()
    model = KMeans(K)
    model.fit(data_ndarray)
    clustering = model.labels_
    centroids = model.cluster_centers_
    final_centroids = R_O.Remove_cluster_one(clustering, K, centroids, data_ndarray.shape[0])
    #closest_points_index_list, value = pairwise_distances_argmin_min(centroids, data_ndarray)
    closest_points_index_list, value = pairwise_distances_argmin_min(final_centroids, data_ndarray)
    #logger.debug(str(closest_points_index_list))

    return clustering, centroids, closest_points_index_list


#******************************************************************************************
#     Function description: Get top N important characteristics for each cluster.         *
#     Input:   K_num, news_clustering, news_centroids.                                    *
#     Return:  clusters_charact_2dlist: (list of dictionery).                             *
#              [{('charac_words', weight), ('charac_words', weight), ...},                *
#               {...}, ...,                                                               *
#               {('charac_words', weight), ('charac_words', weight), ...}]                *
#              Dimention:(N * 20).                                                        *
#******************************************************************************************
def summarize_clusters_characs_2dlist(K_num, news_terms, news_clustering, news_centroids, charac_selec_num):
    clusters_charact_2dlist = []
    for cluster_centroid in news_centroids:
        cluster_charact_index_list = list( f_get_sorted_index_array(np.array(cluster_centroid), charac_selec_num) )
        clusters_charact_temp_dic = {}
        for cluster_charact_index in cluster_charact_index_list:
            clusters_charact_temp_dic[news_terms[cluster_charact_index]] = cluster_centroid[cluster_charact_index]
        clusters_charact_temp_dic = drop_useless_words(clusters_charact_temp_dic)
        clusters_charact_2dlist.append(clusters_charact_temp_dic)
    return clusters_charact_2dlist


#******************************************************************************************
#     Function description: Get N characteristics for overall dataset,                    *
#                               from clusters' characteristics' matrix.                   *
#     Input:   K_num, news_clustering, news_centroids,                                    *
#              clusters_charact_2dlist.                                                   *
#     Return:  overall_charact_words_dic: (dictionery)                                    *
#              {('charac_words', weight),                                                 *
#                ... ,                                                                    *
#               ('charac_words', weight) }                                                *
#******************************************************************************************

def summarize_clusters_characs_clustering(K_num, news_clustering, news_centroids, clusters_charact_2dlist, charac_selec_num):
    # Method-2: Use new important dimentions according each clusters.
    overall_charact_words_dic = {}
    while (len(overall_charact_words_dic) < charac_selec_num):
        cluster_index = 0
        for cluster_centroid in news_centroids:
            cluster_centroid_charac_dic = clusters_charact_2dlist[cluster_index]
            slelct_charac_key = max(cluster_centroid_charac_dic.items(), key=operator.itemgetter(1))[0]
            if slelct_charac_key not in list(overall_charact_words_dic.keys()):
                overall_charact_words_dic[slelct_charac_key] = cluster_centroid_charac_dic[slelct_charac_key]
                del (clusters_charact_2dlist[cluster_index])[slelct_charac_key]
            cluster_index += 1
    #logger.debug(str(len(overall_charact_words_dic)))
    #logger.debug(str(overall_charact_words_dic))
    return overall_charact_words_dic   # {('charac_words', weight), ()}


# ******************************************************************************************
#     Function description: draw data in 16 dimentions with clustering.                   *
#     Input:   news_clustering,                                                           *
#              news_centroids.                                                            *
#              overall_charact_words_dic: (dictionery)                                    *
#              {('charac_words', weight),                                                 *
#                ... ,                                                                    *
#               ('charac_words', weight) }                                                *
# ******************************************************************************************
def f_cluster_plot(news_terms_ndarray, K_num, closest_points_index_list):
    pca = PCA(n_components=2).fit(news_terms_ndarray)
    pca_result2D = pca.transform(news_terms_ndarray)

    pca_nearest_points_array = pca_result2D[closest_points_index_list,:]
    #logger.debug((pca_nearest_points_array.shape))

    # After lower dimension, I used the KMeans to clustering it
    model = KMeans(K_num)
    model.fit(pca_result2D)

    #PCA_km.fit(TFIDF_M)
    clustering = model.labels_
    centroids = model.cluster_centers_

    closest_points_index_list_pca, _ = pairwise_distances_argmin_min(centroids, pca_result2D)
    pca_nearest_points_array_2d = pca_result2D[closest_points_index_list_pca, :]
    #logger.debug(str(closest_points_index_list_pca))

    plt.scatter(pca_result2D[:, 0], pca_result2D[:, 1], c=clustering, s=30, cmap='rainbow')
    plt.scatter(centroids[:,0], centroids[:,1], marker='x', s=50, linewidths=3, color='orange', zorder=10)
    plt.scatter(pca_nearest_points_array[:, 0], pca_nearest_points_array[:, 1], marker='x', s=40, linewidths=2, color='blue', zorder=10)
    plt.scatter(pca_nearest_points_array_2d[:, 0], pca_nearest_points_array_2d[:, 1], marker='x', s=40, linewidths=2, color='red', zorder=10)
    plt.show()

    return closest_points_index_list_pca

#******************************************************************************************
#     Function description: Show different clusters' centroids'  characteristics:         *
#     Input:   news_clustering,                                                           *
#              news_centroids.                                                            *
#              overall_charact_words_dic: (dictionery)                                    *
#              {('charac_words', weight),                                                 *
#                ... ,                                                                    *
#               ('charac_words', weight) }                                                *
#******************************************************************************************
'''
def show_clusters_characs(news_terms, news_clustering, news_centroids, overall_charact_words_dic):
    print("Now print all characteristics' weight in different centroids:")
    cludter_index = 0
    for cluster_centroid in news_centroids:
        print("\tClut_%d\t" % cludter_index, end='', flush=True)
        cludter_index += 1
    print("\n", end='', flush=True)

    for charact_words_key in overall_charact_words_dic.keys():
        print(charact_words_key + '\t: ', end='', flush=True)
        for cluster_centroid in news_centroids:
            print('%.4f\t' % cluster_centroid[ news_terms.index(charact_words_key)], end='', flush=True)
        print("\n", end='', flush=True)
'''

#******************************************************************************************
#     Function description: Final summarization of each cluster's top characteristics.    *
#     Input:   news_clustering,                                                           *
#              news_centroids.                                                            *
#              clusters_charact_2dlist: (list of dictionery).                             *
#              [{('charac_words', weight), ('charac_words', weight), ...},                *
#               {...}, ...,                                                               *
#               {('charac_words', weight), ('charac_words', weight), ...}]                *
#              Dimention:(N * 20).                                                        *
#******************************************************************************************

def summarize_clusters_characs(news_clustering, news_centroids, clusters_charact_2dlist, charac_final_num):
    logger.debug("\n\tFinal summarization of each cluster's characteristics:")
    cluster_index = 0
    for cluster_centroid in news_centroids:
        cluster_charac_words_dic = clusters_charact_2dlist[cluster_index]
        logger.debug("\tClut_" + str(cluster_index) + ":")
        # Select top N characteristics according dic's values.
        top_characs = sorted(cluster_charac_words_dic, key=cluster_charac_words_dic.__getitem__, reverse=True)[0:charac_final_num]
        logger.debug(str(top_characs))
        cluster_index += 1


# ******************************************************************************************
#    Function description: Main body of testing controlling for K-means algorithm.        *
# ******************************************************************************************
def f_k_means_test(news_terms_ndarray, news_terms, K_num):
    charac_selec_num = min(100, len(news_terms))  # All items are selected
    charac_final_num = 20

    news_clustering, news_centroids, closest_points_index_list = f_k_meanCluster(news_terms_ndarray, K_num)

    # Get a 2-D data with each row is a cluster's top characs' dic.
    clusters_charact_2dlist = summarize_clusters_characs_2dlist(K_num, news_terms, news_clustering, news_centroids, charac_selec_num)

    # Get a dic of common top characs for all clusters.
    #overall_charact_words_dic = summarize_clusters_characs_clustering(K_num, news_clustering, news_centroids, clusters_charact_2dlist, charac_selec_num)
    # Now draw all data in common-top-characs' dimentions.
    #show_clusters_characs(news_terms, news_clustering, news_centroids, overall_charact_words_dic)

    #summarize_clusters_characs(news_clustering, news_centroids, clusters_charact_2dlist, charac_final_num)
    closest_points_index_list_pca = None
    #closest_points_index_list_pca = f_cluster_plot(news_terms_ndarray, K_num, closest_points_index_list)

    return closest_points_index_list, closest_points_index_list_pca


class Com_similarity:
    def lemma_tokenizer_v2(ori_news_list):
        # use the standard scikit-learn tokenizer first
        standard_tokenizer = CountVectorizer().build_tokenizer()
        tokens = standard_tokenizer(ori_news_list)
        # then use NLTK to perform lemmatisation on each token
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemma_tokens = []
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                lemma_token = lemmatizer.lemmatize(token)
                if len(lemma_token) > 2:
                    lemma_tokens.append(lemma_token)
        return lemma_tokens

    def relevent_detection(self, news_obj_list):
        try:
            news_documents = []

            for news_obj in news_obj_list:
                if news_obj.news_summarize is not None:
                    #logger.debug("\t\t#news_sum_len: %d" % len(news_obj.news_summarize))
                    news_documents.append(news_obj.news_summarize.lower())
            #logger.debug("\t# Totally %d news file." % len(news_documents))

            tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.1, stop_words='english', \
                                               use_idf=True, tokenizer=Com_similarity.lemma_tokenizer_v2, ngram_range=(1, 1))
            tfidf_matrix = tfidf_vectorizer.fit_transform(news_documents)  # fit the vectorizer to synopses
            #logger.debug("\t\tThe matrix's shape: " + str(tfidf_matrix.shape))

            news_terms = tfidf_vectorizer.get_feature_names()
            #logger.debug("\t\tVocabulary has " + str(len(news_terms)) + " distinct terms")
            #logger.debug("\t\tterms:" + str(news_terms) )

            '''
            # Get an flat 1-D numpy.array of different terms' weights' summarization from sparse matrix.
            terms_weight_sum_array = (tfidf_matrix.sum(axis=0).getA())[0]
            #logger.debug(str(terms_weight_sum_array))
            
            # Get terms' words according their indexes.
            target_words_num = 20
            sorted_index_array = f_get_sorted_index_array(terms_weight_sum_array, target_words_num)
            #logger.debug(str(sorted_index_array))
            
            charact_words_dictionary = {}
            logger.debug("\tThe top 50 most characteristic terms are:")
            logger.debug("\tTerms\tIndex\tWeight")
            for sorted_index in sorted_index_array:
                charact_words_dictionary[news_terms[sorted_index]] = sorted_index
                logger.debug("\t" + str(news_terms[sorted_index]) \
                      + "\t:" + str(sorted_index) \
                      + "\t,%.4f" % terms_weight_sum_array[sorted_index])
            #drop_useless_words(charact_words_dictionary)
            '''

            # Note: the 's' parameter controls the size of the points
            news_terms_ndarray = tfidf_matrix.toarray()
            logger.info("\t\tnews_terms_ndarray's shape is: " + str(news_terms_ndarray.shape))

            # Clustering for 1 group.
            K_num = 2
            closest_points_index_list, closest_points_index_list_pca = f_k_means_test(news_terms_ndarray, news_terms, K_num)

            logger.debug("\tclosest_points_index_list:" + str(closest_points_index_list))
            idx = 0
            for closest_points_index in closest_points_index_list:
                idx = idx + 1
                logger.info("Centroid -" + str(idx) + "- nearest News-" + str(news_obj_list[closest_points_index].id) + "-: " + str(news_obj_list[closest_points_index].news_title))

            '''
            logger.debug("\tclosest_points_index_list_pca:" + str(closest_points_index_list_pca))
            idx = 0
            for closest_points_index in closest_points_index_list_pca:
                idx = idx + 1
                logger.info("Centroid -" + str(idx) + "- nearest News-" + str(news_obj_list[closest_points_index].id) + "-: " + str(news_obj_list[closest_points_index].news_title))
            '''
            return closest_points_index_list
        except Exception as e:
            logger.error(e)
            return None

    def dynamic_relevent_detection(self, news_obj_list):
        try:
            news_documents = []

            for news_obj in news_obj_list:
                if news_obj.news_summarize is not None:
                    # logger.debug("\t\t#news_sum_len: %d" % len(news_obj.news_summarize))
                    news_documents.append(news_obj.news_summarize.lower())

            tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.1, stop_words='english', \
                                               use_idf=True, tokenizer=Com_similarity.lemma_tokenizer_v2,
                                               ngram_range=(1, 1))
            tfidf_matrix = tfidf_vectorizer.fit_transform(news_documents)  # fit the vectorizer to synopses
            news_terms = tfidf_vectorizer.get_feature_names()

            # Note: the 's' parameter controls the size of the points
            news_terms_ndarray = tfidf_matrix.toarray()
            logger.info("\t\tnews_terms_ndarray's shape is: " + str(news_terms_ndarray.shape))

            # Get suitable clusters' number.
            silh_coef_obj = S_C()
            #k_num_silh_coef_dict = silh_coef_obj.compute_K(news_terms_ndarray)
            k_num_silh_coef_dict = silh_coef_obj.compute_K_elbow(news_terms_ndarray)
            #k_num_silh_coef_dict = silh_coef_obj.elbow_mean_distortion(news_terms_ndarray)
            #K_num = silh_coef_obj.Choose_cluster_number(k_num_silh_coef_dict)
            K_num = silh_coef_obj.silh_coef_and_cluster_num_linear_regression(k_num_silh_coef_dict)
            logger.debug("K_num:-[" + str(K_num) + "]-")

            # Clustering for 1 group.
            #K_num = 2
            closest_points_index_list, closest_points_index_list_pca = f_k_means_test(news_terms_ndarray,
                                                                                      news_terms, K_num)

            logger.debug("\tclosest_points_index_list:" + str(closest_points_index_list))
            idx = 0
            for closest_points_index in closest_points_index_list:
                idx = idx + 1
                logger.info("Centroid -" + str(idx) + "- nearest News-" + str(
                    news_obj_list[closest_points_index].id) + "-: " + str(
                    news_obj_list[closest_points_index].news_title))

            return closest_points_index_list
        except Exception as e:
            logger.error(e)
            return None