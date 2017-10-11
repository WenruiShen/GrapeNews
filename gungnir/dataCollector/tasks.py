# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import dataCollector.Past_news
import dataCollector.Ctime
from dataCollector.model_interfaces import *
from dataCollector.models import Topics_model, Ori_News_model, News_model
import dataCollector.get_topics
import datetime, dateutil.parser
from dataCollector.Com_similarity import Com_similarity
from dataCollector.Similarity import Cosine_similarity
import time
import logging
import dataCollector.remove_Punctuation
import dataCollector.Detect_title

logger = logging.getLogger('dataCollector')

############################################################################
############################################################################
# insert static topic list
@shared_task
def init_insert_static_topic():
    #topic_list = ["European Refugee", "North korea", ]
    #topic_list = ["Trump", "ISIS", "European Refugee", "North korea"]
    topic_list = ["Battle Mosul"]
    try:
        topic = Model_Interfaces.db2_add_new_topics(topic_list)
    except Exception as e:
        logger.error("init_insert_static_topic failed: " + str(e))

# insert dynamic topic from wikipedia portal current events
@shared_task
def insert_one_day_hot_Wiki_topic(N_day):
    try:
        A = dataCollector.get_topics.topics()
        raw = A.get_response(N_day)
        #logger.debug(str(raw))
        topic_list = A.pares_raw_data_3(raw)
        time.sleep(5)
        if topic_list is None:
            return
        if len(topic_list) >= 1:
            logger.info("[Day-" + str(N_day) + "'s topics list]: " + str(topic_list))
            logger.info("\t[Get topics_list len]: " + (str(len(topic_list)) if ( topic_list is not None)else 0))
            #test_max_len = min(len(topic_list), 6)
            #Model_Interfaces.db2_add_new_topics(topic_list[:test_max_len])
            Model_Interfaces.db2_add_new_topics(topic_list)
        else:
            return
    except Exception as e:
        logger.error("insert_one_day_hot_Wiki_topic failed: " + str(e))

# insert N_days dynamic topic from wikipedia portal current events
@shared_task
def insert_N_days_hot_Wiki_topics(N_days):
    for N_day in range(N_days-1, 0, -1):
        insert_one_day_hot_Wiki_topic(N_day)


# get All topic from topic table function V1.0
@shared_task
def get_topic():
    start_id = 1
    amount = 1
    All_topic = []
    topic_time = []
    topic_id = []
    try:
        while True:
            topic_list, topic_amount, topic_count, last_id = Model_Interfaces.db2_get_all_topics(start_id, amount)
            if last_id is None:
                break
            start_id = last_id + 1
            All_topic.append(topic_list[0].topic_name)
            topic_time.append(str(topic_list[0].latest_update_time))
            topic_id.append(topic_list[0].id)
        return All_topic,topic_time,topic_id
    except Exception as e:
        logger.error("get_topic failed: " + str(e))
        return None, None, None

# get all topic from topic table function V2.0
@shared_task
def get_topic_V2():
    topic_id = []
    All_topic = []
    topic_time = []
    try:
        topic_list = Model_Interfaces.db2_get_all_topicsv2()
        for x in topic_list:
            topic_id.append(x.id)
            All_topic.append(x.topic_name)
            topic_time.append(str(x.latest_update_time))
        return All_topic,topic_time,topic_id
    except Exception as e:
        logger.error("get_topic_V2 failed: " + str(e))
        return None, None, None

# get latest topic V1.0
@shared_task
def get_latest_topic():
    All_topic = []
    #topic_time = []
    topic_id = []
    try:
        #latest_topic = Model_Interfaces.db2_get_all_latest_topics(datetime.date.today())
        latest_topic = Model_Interfaces.db2_get_recent_hot_topic()
        if latest_topic is not None:
            for i in range(0,len(latest_topic)):
                #logger.debug(latest_topic[i].latest_update_time)
                if latest_topic[i].latest_update_time is None:
                    latest_topic_name = latest_topic[i].topic_name
                    latest_id = latest_topic[i].id
                    All_topic.append(latest_topic_name)
                    topic_id.append(latest_id)
            return All_topic, topic_id
        else:
            return None, None
    except Exception as e:
        logger.error("get_latest_topic failed: " + str(e))
        return  None, None


# add_daily news from BBC CNN ABC and NYT V2.0
@shared_task
def add_daily_processing():
    try:
        # Get all topic from topic table
        All_topic, All_time, All_id = get_topic_V2()
        b = dataCollector.Past_news.ALL_news()
        # Processed each topic (remove stopwords)
        remove = dataCollector.remove_Punctuation.Remove()
        if All_topic is not None:
            # generate today's zero time such as 2017.7.20.00:00:00.000Z
            now_time = dateutil.parser.parse(str(datetime.datetime.now())[0:11] + "00:00:00.000Z")
            yes_time = now_time + datetime.timedelta(days=-3)
            yes_time_nyr = yes_time.strftime('%Y%m%d')
            for x, y, z in zip(All_topic, All_time, All_id):
                logger.info("\t[topic]:" + str(x))
                news_content_list = []
                news_summary_list = []
                time_list = []
                title_list = []
                url_list = []
                image_list = []
                temple = y
                # judge latest update
                if (temple == "None"):
                    latest_update = str(datetime.datetime.now())[0:10] + "T00:00:00.000Z"
                else:
                    latest_update = str(y)

                # Page control.
                clear_x = remove.removestopword(x)
                BBC_empty_mark = 0
                NYT_empty_mark = 0
                ABC_empty_mark = 0
                CNN_empty_mark = 0

                # retrive 2 pages for today.
                for p in range(1, 3):
                    #logger.debug("\tPage:%d" % p)
                    # BBC extraction
                    if BBC_empty_mark is 0:
                        Bnews_content, Bnews_summary, Btimes, Btitles, Burl, Bnews_image = b.BBC_news_search_get(clear_x, p, latest_update)
                        if len(Bnews_content) is not 0:
                            news_content_list = news_content_list + Bnews_content
                            news_summary_list = news_summary_list + Bnews_summary
                            time_list = time_list + Btimes
                            title_list = title_list + Btitles
                            url_list = url_list + Burl
                            image_list = image_list + Bnews_image
                        else:
                            # Can not get data from BBC.
                            BBC_empty_mark = 1
                        #logger.debug("\tBBC done")

                    # ABC extraction
                    if ABC_empty_mark is 0:
                        Anews_content, Anews_summary, Atimes, Atitles, Aurl, Anews_image = b.ABC_news_search_get(clear_x, p-1, latest_update)
                        if len(Anews_content) is not 0:
                            news_content_list = news_content_list + Anews_content
                            news_summary_list = news_summary_list + Anews_summary
                            time_list = time_list + Atimes
                            title_list = title_list + Atitles
                            url_list = url_list + Aurl
                            image_list = image_list + Anews_image
                        else:
                            # Can not get data from BBC.
                            ABC_empty_mark = 1
                        #logger.debug("\tABC done")

                    # CNN extraction
                    if CNN_empty_mark is 0:
                        Cnews_content, Cnews_summary, Ctimes, Ctitles, Curl, Cnews_image = b.CNN_news_search_get(str(clear_x), p, latest_update)
                        if len(Cnews_content) is not 0:
                            news_content_list = news_content_list + Cnews_content
                            news_summary_list = news_summary_list + Cnews_summary
                            time_list = time_list + Ctimes
                            title_list = title_list + Ctitles
                            url_list = url_list + Curl
                            image_list = image_list + Cnews_image
                        else:
                            # Can not get data from BBC.
                            CNN_empty_mark = 1
                        #logger.debug("\tCNN done")


                    # NYT extraction
                    if NYT_empty_mark is 0:
                        Nnews_content, Nnews_summary, Ntimes, Ntitles, Nurl, Nnews_image = b.NYT_news_search_get(clear_x, (p-1), latest_update)
                        if len(Nnews_content) is not 0:
                            news_content_list = news_content_list + Nnews_content
                            news_summary_list = news_summary_list + Nnews_summary
                            time_list = time_list + Ntimes
                            title_list = title_list + Ntitles
                            url_list = url_list + Nurl
                            image_list = image_list + Nnews_image
                        else:
                            # Can not get data from NYT.
                            NYT_empty_mark = 1
                        #logger.debug("\tNYT done")

                    # Deply for avoiding http request too frequently;
                    #time.sleep(0.3)

                # Pre-filter outlier news.
                ori_len = len(news_content_list)
                detect_obj = dataCollector.Detect_title.title_()
                res_list = detect_obj.compare_title(title_list, clear_x, news_content_list)

                filter_news_content_list = []
                filter_news_summary_list = []
                filter_time_list = []
                filter_title_list = []
                filter_url_list = []
                filter_image_list = []

                for res_index in res_list:
                    filter_news_content_list.append(news_content_list[res_index])
                    filter_news_summary_list.append(news_summary_list[res_index])
                    filter_time_list.append(time_list[res_index])
                    filter_title_list.append(title_list[res_index])
                    filter_url_list.append(url_list[res_index])
                    filter_image_list.append(image_list[res_index])

                logger.info("\t[Get daily news] ori_num:" + str(ori_len) + ";\tfilter_num:"+ str(len(filter_news_content_list)) )
                # Insert daily news into original news table
                for content, summary, times, title, url, image in zip(filter_news_content_list, filter_news_summary_list, filter_time_list, filter_title_list, filter_url_list, filter_image_list):
                    Model_Interfaces.db2_add_one_ori_news(dateutil.parser.parse(times), str(title), str(content), str(summary), str(z), str(url), str(image))
    except Exception as e:
        logger.error("add_daily_processing failed: " + str(e))

# add history news from BBC and NYT V2.0
@shared_task
def add_history_processing(history_days):
    try:
        # Get latest topic
        topic_name_list, All_id = get_latest_topic()
        b = dataCollector.Past_news.ALL_news()
        # Process topic (Remove stopwords)
        remove = dataCollector.remove_Punctuation.Remove()
        if topic_name_list is not None:
            now_time = dateutil.parser.parse(str(datetime.datetime.now())[0:11] + "00:00:00.000Z")
            # Generate history start time
            start_date = now_time + datetime.timedelta(days=-history_days)
            start_date_nyr = start_date.strftime('%Y%m%d')
            for x, z in zip(topic_name_list, All_id):
                logger.info("\t[topic]:" + str(x))
                news_content_list = []
                news_summary_list = []
                time_list = []
                title_list = []
                url_list = []
                image_list = []

                clear_x = remove.removestopword(x)
                BBC_empty_mark = 0
                NYT_empty_mark = 0
                ABC_empty_mark = 0
                CNN_empty_mark = 0

                # retrive max 10 pages for history.
                for p in range(1, 10):
                    logger.debug("\tPage:%d" % p)
                    # BBC extraction
                    if BBC_empty_mark is 0:
                        Bnews_content, Bnews_summary, Btimes, Btitles, Burl, Bnews_image = b.BBC_news_search_get(str(clear_x), p, str(start_date))
                        if len(Bnews_content) is not 0:
                            news_content_list = news_content_list + Bnews_content
                            news_summary_list = news_summary_list + Bnews_summary
                            time_list = time_list + Btimes
                            title_list = title_list + Btitles
                            url_list = url_list + Burl
                            image_list = image_list + Bnews_image
                        else:
                            # Can not get data from BBC.
                            BBC_empty_mark = 1
                    logger.debug("\tBBC done")

                    '''
                    # ABC extraction
                    if ABC_empty_mark is 0:
                        Anews_content, Anews_summary, Atimes, Atitles, Aurl, Anews_image = b.ABC_news_search_get(clear_x, p-1, str(start_date))
                        if len(Anews_content) is not 0:
                            news_content_list = news_content_list + Anews_content
                            news_summary_list = news_summary_list + Anews_summary
                            time_list = time_list + Atimes
                            title_list = title_list + Atitles
                            url_list = url_list + Aurl
                            image_list = image_list + Anews_image
                        else:
                            # Can not get data from BBC.
                            ABC_empty_mark = 1
                    logger.debug("\tABC done")
                    '''

                    # CNN extraction
                    if CNN_empty_mark is 0:
                        Cnews_content, Cnews_summary, Ctimes, Ctitles, Curl, Cnews_image = b.CNN_news_search_get(str(clear_x), p, str(start_date))
                        if len(Cnews_content) is not 0:
                            news_content_list = news_content_list + Cnews_content
                            news_summary_list = news_summary_list + Cnews_summary
                            time_list = time_list + Ctimes
                            title_list = title_list + Ctitles
                            url_list = url_list + Curl
                            image_list = image_list + Cnews_image
                        else:
                            # Can not get data from BBC.
                            CNN_empty_mark = 1
                        logger.debug("\tCNN done")

                    # NYT extraction

                    if NYT_empty_mark is 0:
                        Nnews_content, Nnews_summary, Ntimes, Ntitles, Nurl, Nnews_image = b.NYT_news_search_get(str(clear_x), (p-1), str(start_date))
                        if len(Nnews_content) is not 0:
                            news_content_list = news_content_list + Nnews_content
                            news_summary_list = news_summary_list + Nnews_summary
                            time_list = time_list + Ntimes
                            title_list = title_list + Ntitles
                            url_list = url_list + Nurl
                            image_list = image_list + Nnews_image
                        else:
                            # Can not get data from NYT.
                            NYT_empty_mark = 1
                        logger.debug("\tNYT done")


                    # Deply for avoiding http request too frequently;
                    #time.sleep(0.3)

                # Pre-filter outlier news.
                ori_len = len(news_content_list)
                detect_obj = dataCollector.Detect_title.title_()
                res_list = detect_obj.compare_title(title_list, clear_x, news_content_list)

                filter_news_content_list = []
                filter_news_summary_list = []
                filter_time_list = []
                filter_title_list = []
                filter_url_list = []
                filter_image_list = []

                for res_index in res_list:
                    filter_news_content_list.append(news_content_list[res_index])
                    filter_news_summary_list.append(news_summary_list[res_index])
                    filter_time_list.append(time_list[res_index])
                    filter_title_list.append(title_list[res_index])
                    filter_url_list.append(url_list[res_index])
                    filter_image_list.append(image_list[res_index])

                logger.info("\t[Get history news] ori_num:" + str(ori_len) + ";\tfilter_num:"+ str(len(filter_news_content_list)) )
                # Insert history news into original news table
                for content, summary, times, title, url, image in zip(filter_news_content_list, filter_news_summary_list, filter_time_list, filter_title_list, filter_url_list, filter_image_list):
                    Model_Interfaces.db2_add_one_ori_news(dateutil.parser.parse(times), str(title), str(content), str(summary), str(z), str(url), str(image))
    except Exception as e:
        logger.error("add_history_processing failed: " + str(e))


@shared_task
# dynamic cluster in one topic news
def one_topic_news_dynamic_cluster_flow(topic):
    try:
        if topic is None:
            return None
        news_obj_under_topic_set = Model_Interfaces.db2_get_ori_news_of_one_topic(topic.id)
        if news_obj_under_topic_set is None:
            return

        logger.info("\n###########################################################\n" + \
                            "one_topic_news_dynamic_cluster_flow \ttopic.id=" + str(topic.id) + \
                            ";\tname: \"" + str(topic.topic_name) + \
                            "\";\tnews_len: " + str(len(news_obj_under_topic_set)) + \
                            ";\tlatest_cluster_time:" + str(topic.latest_cluster_time) )

        if topic.latest_cluster_time is not None:
            topic_latest_cluster_date = topic.latest_cluster_time.date()
            # Delete latest few days filtered news_DB news, avoiding duplicated insert.
            News_model.objects.all().filter(news_topic=topic).filter(news_date__date__gt=topic_latest_cluster_date).delete()
        else:
            topic_latest_cluster_date = None

        # Reverse the order by date.
        news_obj_under_topic_list = list(news_obj_under_topic_set)[::-1]

        # Now iterate all news under this topic.
        one_week_time_delta = datetime.timedelta(days=1)
        total_news_num = len(news_obj_under_topic_list)
        clustered_id_start = 0
        while clustered_id_start < total_news_num:
            news_date_start = news_obj_under_topic_list[clustered_id_start].news_date.date()

            # Charge whether this news has been filtered.
            if topic_latest_cluster_date is not None:
                if news_date_start <= topic_latest_cluster_date:
                    logger.debug("-Filtered: \t" + str(news_date_start))
                    clustered_id_start = clustered_id_start + 1
                    continue

            clustered_id_end = clustered_id_start + 1
            # Get news within one week.
            while clustered_id_end < total_news_num:
                news_date_end = news_obj_under_topic_list[clustered_id_end].news_date.date()
                if news_date_end > news_date_start + one_week_time_delta:
                    break
                clustered_id_end = clustered_id_end + 1

            if clustered_id_start + 1 >= clustered_id_end:
                logger.debug("-Single: \t" + str(news_date_start))
                # Should insert news into new news DB here.
                single_news = news_obj_under_topic_list[clustered_id_start]
                Model_Interfaces.db2_add_one_filter_news(single_news.news_date, \
                                                         single_news.news_title, \
                                                         single_news.news_summarize, \
                                                         topic.id, \
                                                         single_news.news_url, \
                                                         single_news.image_url)
                clustered_id_start = clustered_id_end
                continue

            cluster_news_list = news_obj_under_topic_list[clustered_id_start:clustered_id_end]
            selected_news_list = []
            if len(cluster_news_list) > 3:
                Com_similarity_obj = Com_similarity()
                closest_points_index_list = Com_similarity_obj.dynamic_relevent_detection(cluster_news_list)
                logger.info("-Clustering: from: " + str(cluster_news_list[0].news_date.date()) + \
                            "\t to:" + str(news_date_end) + \
                             ";\tBefore:" + str(len(cluster_news_list)) + \
                             ";\tAfter:" + str(len(closest_points_index_list)) + "\n")
                if closest_points_index_list is not None:
                    for index in closest_points_index_list:
                        selected_news_list.append(cluster_news_list[index])
                #selected_news_list = cluster_news_list
            else:
                Cosine_similarity_obj = Cosine_similarity()
                closest_points_index_list = Cosine_similarity_obj.comput_cosine_similarity(cluster_news_list)
                logger.info("-A few: from: " + str(cluster_news_list[0].news_date.date()) + \
                             "\t to:" + str(news_date_end) + \
                             ";\tBefore:" + str(len(cluster_news_list)) + \
                             ";\tAfter:" + str(len(closest_points_index_list)) + "\n")
                if closest_points_index_list is not None:
                    for index in closest_points_index_list:
                        selected_news_list.append(cluster_news_list[index])
                #selected_news_list = cluster_news_list

            # Should insert news into new news DB here.
            for cluster_news in selected_news_list:
                if cluster_news is not None:
                    Model_Interfaces.db2_add_one_filter_news(cluster_news.news_date, \
                                                             cluster_news.news_title, \
                                                             cluster_news.news_summarize, \
                                                             topic.id, \
                                                             cluster_news.news_url, \
                                                             cluster_news.image_url)
            clustered_id_start = clustered_id_end

        # Update topic.latest_cluster_time to yesterday.
        Model_Interfaces.db2_topic_update_latest_cluster_time(topic.id, news_obj_under_topic_list[total_news_num - 1].news_date - one_week_time_delta)
    except Exception as e:
        logger.error("one_topic_news_dynamic_cluster_flow() failed: " + str(e))


@shared_task
def cluster_flow():
    try:
        topics_set = Model_Interfaces.db2_get_recent_hot_topic()
        if topics_set is None:
            return None
        if len(topics_set) == 0:
            return None
        for topic in topics_set:
            one_topic_news_dynamic_cluster_flow(topic)
    except Exception as e:
        logger.error("cluster_test_flow() failed: " + str(e))

@shared_task
def all_latest_cluster_time_mark_clean():
    try:
        topics_set = Model_Interfaces.db2_get_recent_hot_topic()
        if topics_set is None:
            return None
        if len(topics_set) == 0:
            return None
        for test_topic in topics_set:
            test_topic.latest_filter_time = None
            test_topic.latest_cluster_time = None
            test_topic.save()
            Model_Interfaces.db2_get_filter_news_of_one_topic(test_topic.id).delete()
    except Exception as e:
        logger.error("cluster_test_flow() failed: " + str(e))

@shared_task
def cluster_test_flow():
    try:
        test_topic_name = "White House Press Secretary"
        test_topic = Topics_model.db_get_one_topic_by_name(test_topic_name)
        if test_topic is None:
            return None
        one_topic_news_dynamic_cluster_flow(test_topic)
    except Exception as e:
        logger.error("cluster_test_flow() failed: " + str(e))


@shared_task
def latest_cluster_time_mark_clean():
    try:
        test_topic_name = "White House Press Secretary"
        test_topic = Topics_model.db_get_one_topic_by_name(test_topic_name)
        if test_topic is None:
            return None
        test_topic.latest_filter_time = None
        test_topic.latest_cluster_time = None
        test_topic.save()

        Model_Interfaces.db2_get_filter_news_of_one_topic(test_topic.id).delete()
    except Exception as e:
        logger.error("latest_cluster_time_mark_clean() failed: " + str(e))

@shared_task
def flow_opt(N_days):
    try:
        logger.info("\n##############################################################\n" +
                    "\t-- flow_opt() start: " + str(datetime.datetime.now()) +
                    "\n---------------------------------------------------------------\n")
        if N_days is None:
            logger.error("flow_opt() failed, N_days: " + str(N_days))
            return

        insert_N_days_hot_Wiki_topics(N_days)
        logger.info("-- insert_topic_Wiki [" + str(N_days) + "] days done: " + str(datetime.datetime.now()))

        history_days = 60
        add_history_processing(history_days)
        logger.info(
            "-- add_history_processing [" + str(history_days) + "] days done: " + str(datetime.datetime.now()))

        add_daily_processing()
        logger.info("-- add_daily_processing done: " + str(datetime.datetime.now()))

        Model_Interfaces.db2_delete_all_topics_without_news()
        logger.info("-- db2_delete_all_topics_without_news done.")

        cluster_flow()
        logger.info("-- cluster_flow done.")

        logger.info("\n---------------------------------------------------------------\n" +
                    "\t-- flow_opt() done: " + str(datetime.datetime.now()) +
                    "\n##############################################################\n")
    except Exception as e:
        logger.error("flow_opt() failed: " + str(e))

# schedule task
@shared_task
def flow():
    N_days = 3
    flow_opt(N_days)

# schedule task
@shared_task
def init_flow():
    try:
        #init_insert_static_topic()
        #logger.debug("Init_insert_static_topic over!")
        N_days = 10
        flow_opt(N_days)
        logger.debug("init_flow() over.")
    except Exception as e:
        logger.error("init_flow() failed: " + str(e))
