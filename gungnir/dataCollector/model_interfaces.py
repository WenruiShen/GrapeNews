###########################################################
#     User interfaces for UCD-project's databases:
#         Author: Wenrui Shen 15210671, Hong Su 15211605
#         Date:     2017-06-05
#        Version: 1.1
#        Description:    2nd layer interfaces;
###########################################################
from django.db import models
from dataCollector.models import Topics_model, Ori_News_model, News_model
#import datetime
from django.utils import timezone
import logging

logger = logging.getLogger('dataCollector')

class Model_Interfaces():
    # 4.2.1.1
    def db2_add_new_topics(topic_name_list):
        flag = -1
        add_list = []
        fail_list = []
        if topic_name_list is not None:
            try:
                for name in topic_name_list:
                    topic = Topics_model.db_insert_one_topic(name)
                    if topic == None:
                        fail_list.append(name)
                        flag = 0
                    else:
                        add_list.append(name)
                if add_list == topic_name_list:
                    flag = 1
                for e_name in fail_list:
                    topic = Topics_model.db_get_one_topic_by_name(e_name)
                    if topic is not None:
                        topic.db_update_recent_hot_date()
            except Exception as e:
                logger.error("db2_add_new_topics failed: " + str(e))
                return flag, add_list, fail_list
        return flag, add_list, fail_list

    # 4.2.1.2.1 get the topics which are hot right now.
    def db2_get_all_latest_topics( date_input):
        topic_list = Topics_model.db_get_all_recent_hot_topics(date_input)
        return topic_list
    
    # 4.2.1.2.2 Get only new exist topics (Exclude existed before):
    def db2_get_only_latest_topics(date_input):
        topic_list = Topics_model.db_get_all_topics_created_before_date(date_input)
        return topic_list

    # 4.2.1.2.3 Get all old topics:(Including duplicated topics):
    def db2_get_all_old_topics(start_id, amount, date_input):
        return_list = []
        count = 0
        last_id = None
        topic_list = Topics_model.db_get_all_topics_created_before_date(date_input)
        for topic in topic_list:
            if topic.id in range(start_id, start_id+amount):
                return_list.append(topic)
                count = count + 1
                last_id = topic.id
        return return_list, amount,count, last_id

    # 4.2.1.2.4 Get all topics(Both old and latest)
    def db2_get_all_topics(start_id, amount):
        topic_list = []
        count = 0
        last_id = None
        for i in range(start_id, start_id+amount):
            topic = Topics_model.db_get_one_topic_by_id(i)
            if topic is not None:
                topic_list.append(topic)
                count = count + 1
                last_id = topic.id
        return topic_list, amount ,count, last_id

    # 4.2.1.2.5 Get all topics(Both old and latest)
    def db2_get_all_topicsv2():
        topics_list = Topics_model.db_get_all_topics()
        if topics_list is not None:
            return topics_list
        else:
            return None

    # 4.2.1.2.6 Get recent hot topic:
    def db2_get_recent_hot_topic():
        topic_set = Topics_model.db_get_recent_hot_topics()
        if topic_set is not None:
            return topic_set
        else:
            return None

    # 4.2.1.2.7 Get recent hot topic:
    def db2_get_recent_hot_topic_rest():
        topic_set = Topics_model.db_get_recent_hot_topics_rest()
        if topic_set is not None:
            return topic_set
        else:
            return None

    # 4.2.1.2.8 Get top n recent hot topic:
    def db2_get_n_recent_hot_topic_rest(topics_num, topics_start):
        topic_set = Topics_model.db_get_n_recent_hot_topics_rest(topics_num, topics_start)
        if topic_set is not None:
            return topic_set
        else:
            return None

    # Delete all topics which do not have any news.
    def db2_delete_all_topics_without_news():
        Topics_model.db_delete_all_topics_without_news()


    # 4.2.2.1.1 Add one original news info
    def db2_add_one_ori_news(news_date,news_title,news_content,news_summary,news_topic_id,news_url,image_rul):
        if len(news_content) < 200:
            return None
        if len(image_rul) < 3:
            return None
        flag = -1
        topic = Topics_model.db_get_one_topic_by_id(news_topic_id)
        if topic is not None:
            news = Ori_News_model.db_insert_one_news(news_title,news_date, news_content,news_summary,news_url,topic,image_rul)
            if news is not None:
                flag =1
                topic.latest_update_time = timezone.now()
                topic = Topics_model.db_update_one_topic(topic)
        else:
            news = None
            topic = None
        return flag, news, topic

    # 4.2.2.1.1 Add one filtered news info
    def db2_add_one_filter_news(news_date, news_title, news_summary, news_topic_id, news_url, image_rul):
        if len(news_summary) < 200:
            return None
        if len(image_rul) < 3:
            return None
        flag = -1
        topic = Topics_model.db_get_one_topic_by_id(news_topic_id)
        if topic is not None:
            news = News_model.db_insert_one_news(news_title, news_date, news_summary, news_url, topic, image_rul)
            if news is not None:
                flag = 1
                topic.latest_filter_time = timezone.now()
                topic2 = Topics_model.db_update_one_topic(topic)
        else:
            news = None
            topic = None
        return flag, news, topic

    # 4.2.2.2.1 Get some original news under one certain topic
    def db2_get_ori_news_of_one_topic(topic_id):
        news_set = Ori_News_model.db_get_news_by_topic_id(topic_id)
        if news_set is not None:
            return news_set
        else:
            return None

    # 4.2.2.2.2 Get some news under one certain topic
    def db2_get_filter_news_of_one_topic(topic_id):
        news_set = News_model.db_get_news_by_topic_id(topic_id)
        if news_set is not None:
            return news_set
        else:
            return None

    # 4.2.2.2.2 Get some news under one certain topic
    #def db2_get_news_of_one_topic(topic_id,max_news_num,start_date,end_date,start_index,end_index):
    def db2_get_n_recent_news_under_one_topic(topic_id, news_num):
        news_set = News_model.db_get_news_by_topic_id(topic_id)
        return list(news_set)[:int(news_num)] if len(news_set) > 0 else None

    # get topic names which contains specified text
    def db2_topics_search(inputValue):
        topic_set = Topics_model.db_search_topics(inputValue)
        # return topic_set if len(topic_set) > 0 else None
        return  topic_set

    def db2_topic_update_latest_cluster_time(topic_id, _latest_cluster_time):
        topic = Topics_model.db_update_latest_cluster_time(topic_id, _latest_cluster_time)
        return topic