# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 16:01:30 2017

@author: Ovenus
"""

import sys
#sys.path.append(r"E:\Gungnir\django_celery\dataCollector")
#import Ccrawling
#Ccrawling.re
#Ccrawling.extract_hot2()
#result = Ccrawling.re
#result.extract_hot()
import time
import dataCollector.Ccreate
import logging

logger = logging.getLogger('dataCollector')

class ALL_news:
    # NYT news extraction
    def NYT_news_search_get(self, query, page, start_date):
        try:
            q = query
            p = page
            t = dataCollector.Ccreate.NYT()
            u2 = t.create_NYTURL_2_1(p,q)
            if u2 is None:
                return None, None, None, None, None
            news_url_list, news_date_list = t.parse_json(u2, start_date)
            new_content, news_summary, pub_time, new_title, news_url, news_image = t.extract_newsV2(news_url_list, news_date_list, start_date)
            return new_content, news_summary, pub_time, new_title, news_url, news_image
        except Exception as e:
            logger.error("NYT_news_search_get failed: " + str(e))
            return None, None, None, None, None, None
        
    # BBC news extraction
    def BBC_news_search_get(self, query, page, start_date):
        try:
            q = query
            p = page
            b = dataCollector.Ccreate.BBC()
            r = b.create_URL_2(p,q)
            if r is None:
                return None, None, None, None, None
            news_url_list, news_date_list = b.extract_pubtime_newsurl(r)
            #logger.debug("\t\t[++len++]:" + str(len(news_date_list)) + ", " + str(len(news_url_list)))
            new_content, news_summary, bb_time, bb_ltie, bb_url, news_image = b.extract_newsV2(news_url_list, news_date_list, start_date)
            return new_content, news_summary, bb_time, bb_ltie, bb_url, news_image
        except Exception as e:
            logger.error("BBC_news_search_get failed: " + str(e))
            return None, None, None, None, None

    # ABC news extraction
    def ABC_news_search_get(self, query, page, start_date):
        try:
            q = query
            p = page
            a = dataCollector.Ccreate.ABC()
            r = a.create_URL2(p,q)
            #logger.debug(str(r))
            if r is None:
                return None, None, None, None, None
            html = a.extract_web(r)
            news_url_list, news_date_list = a.extract_pubtime_newsurl(html)
            #logger.debug("\t\t[++len++]:" + str(len(news_date_list)) + ", " + str(len(news_url_list)))
            new_content, news_summary, abc_time, abc_ltie, abc_url, abc_news_image = a.extract_newsV2(news_url_list, news_date_list, start_date)
            return new_content, news_summary, abc_time, abc_ltie, abc_url, abc_news_image
            #return news_url_list, news_date_list
        except Exception as e:
            logger.error("ABC_news_search_get failed: " + str(e))
            return None, None, None, None, None

    # CNN news extraction
    def CNN_news_search_get(self, query, page, start_date):
        try:
            q = query
            p = page
            c = dataCollector.Ccreate.CNN()
            u2 = c.create_URL2(p,q)
            #logger.debug(str(u2))
            if u2 is None:
                return None, None, None, None, None
            news_url_list, news_date_list = c.parse_json_CNN(u2, start_date)
            #logger.debug(str(news_url_list))
            new_content, news_summary, pub_time, new_title, news_url, news_image = c.extract_newsV2(news_url_list, news_date_list, start_date)
            return new_content, news_summary, pub_time, new_title, news_url, news_image
        except Exception as e:
            logger.error("CNN_news_search_get failed: " + str(e))
            return None, None, None, None, None