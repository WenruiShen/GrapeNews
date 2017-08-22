import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import dataCollector.Remove_outlier
import logging

logger = logging.getLogger('dataCollector')

class Cosine_similarity:
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

    def comput_cosine_similarity(self, news_obj_list):
        try:
            news_documents = []
            for news_obj in news_obj_list:
                if news_obj.news_summarize is not None:
                    news_documents.append(news_obj.news_summarize.lower())
            tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.1, stop_words='english', \
                                               use_idf=True, tokenizer=Cosine_similarity.lemma_tokenizer_v2, ngram_range=(1, 1))
            tfidf_matrix = tfidf_vectorizer.fit_transform(news_documents)

            cos = cosine_similarity(tfidf_matrix)

            R_O = dataCollector.Remove_outlier.R_outlier()
            remove_index = []
            #remove_index = R_O.Remove_outlier_simi(cos)

            row_len = cos.shape[0]
            colum_len = cos.shape[1]
            if row_len != colum_len:
                return None
            if row_len != len(news_obj_list):
                return None

            cos_sim_sum = 0
            cos_sim_mean = 0
            default_similar_cos_sim_threshold = 0.18

            for row_id in range(0, row_len-1):
                if row_id >= colum_len:
                    break
                logger.debug(cos[row_id][row_id+1:colum_len])
                cos_sim_sum = cos_sim_sum + sum(cos[row_id][row_id+1:colum_len])

            cos_sim_mean = cos_sim_sum / (row_len * row_len / 2)
            similar_cos_sim_threshold = max(cos_sim_mean * 2, default_similar_cos_sim_threshold)
            logger.debug("similar_cos_sim_threshold:\t" + str(similar_cos_sim_threshold))

            ori_news_indexs_list = [index for index in range(0, len(news_obj_list))]
            # logger.debug("ori_news_indexs_list:\t" + str(ori_news_indexs_list))

            # remove discrete points.
            logger.debug("remove_index:" + str(remove_index))
            if remove_index is not None:
                for r_index in remove_index:
                    if r_index in ori_news_indexs_list:
                        ori_news_indexs_list.remove(r_index)

            # remove similar points.
            for row_id in range(0, row_len-1):
                if row_id >= colum_len:
                    break
                for colum_id in range(row_id+1, colum_len):
                    if cos[row_id][colum_id] >= similar_cos_sim_threshold:
                        # Remove similar points.
                        if row_id in ori_news_indexs_list:
                            ori_news_indexs_list.remove(row_id)
            news_indexs = ori_news_indexs_list
            logger.debug("reserverd news_indexs:\t" + str(news_indexs))
            return news_indexs
        except Exception as e:
            logger.error(e)
            return None



