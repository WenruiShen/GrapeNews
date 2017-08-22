# -*- coding:utf-8 -*-
import re
from simhash import Simhash
import logging

logger = logging.getLogger('dataCollector')

class Simhash_Filter():
    def get_features(self, s):
        width = 3
        s = s.lower()
        s = re.sub(r'[^\w]+', '', s)
        return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

    def get_distance(self, document1, document2):
        distance = Simhash(document1).distance(Simhash(document2))
        return distance

    def remove_duplicates(self, news_list, time_list, title_list, url_list, image_list):
        index = 0
        '''
        s = Simhash_Filter()
        while (index < len(news_list) - 1):
            index_cp = index + 1
            while (index_cp < len(news_list)):
                #logger.debug(str(url_list[index]) + ", " + str(url_list[index_cp]))
                distance = s.get_distance(news_list[index], news_list[index_cp])
                if distance in range(5):  # range need test
                    news_list.pop(index_cp)
                    time_list.pop(index_cp)
                    title_list.pop(index_cp)
                    url_list.pop(index_cp)
                    image_list.pop(index_cp)
                    #logger.debug(str(url_list[index]) + ", " + str(url_list[index_cp]))
                    #logger.debug(str(index_cp))
                index_cp = index_cp + 1
            index = index + 1
        '''
        return news_list, time_list, title_list, url_list, image_list

