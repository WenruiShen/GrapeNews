from sklearn import feature_extraction
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import re
import logging

logger = logging.getLogger('dataCollector')

class title_:
    def tokenize_and_stem(text):
        stemmer = SnowballStemmer("english")
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems

    def compare_title(self, title_list, topic, content_list):
        res_index = []
        index = 0
        topic_tokens = title_.tokenize_and_stem(topic)
        for title, content in zip(title_list, content_list):
            title_token = title_.tokenize_and_stem(title)
            cut_len = min(max(int(len(content)/2), 8000), len(content))
            #logger.debug("cut_len : " + str(cut_len))
            content_token = title_.tokenize_and_stem(content[0:cut_len])
            mark = 0
            logger.debug("\ttopic_tokens:" + str(topic_tokens) + ";\ttitle:" + str(title))
            for word in topic_tokens:
                if word in title_token:
                    #logger.debug("\t\t\t" + word + ": in title")
                    mark = mark + 1
                #else:
                    #logger.debug("\t\t\t" + word + ": not in title")
            if mark <= 2:
                dict1 = {}
                for word in topic_tokens:
                    if word in content_token:
                        dict1[word] = 1
                logger.debug("\t\tmark == 0; dict1:" + str(dict1))

                if len(dict1) >= min(len(topic_tokens), 4):
                    res_index.append(index)
                    logger.debug("\t\tMATCHING-1: len(dict1):" + str(len(dict1)) + ";\tlen(topic_tokens):" + str(len(topic_tokens)))
            else:
                res_index.append(index)
                logger.debug("\t\tMATCHING-0: len(topic_tokens):" + str(len(topic_tokens)) + ";\tmark=" + str(mark))
            index = index + 1
        return res_index





