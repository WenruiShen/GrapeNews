# require pycharm run config: DJANGO_SETTINGS_MODULE=gungnir.settings
import django
django.setup()

import unittest
from django.utils import timezone
from dataCollector.models import Topics_model,News_model,Ori_News_model
from dataCollector.model_interfaces import Model_Interfaces
from accounts.models import User
from accounts.serializers import UserDetailSerializer
from datetime import timedelta
from django.db.models import Count
import datetime






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework import viewsets

from dataCollector.models import Topics_model,News_model,Ori_News_model
from gungirRest.serializers import TopicsSerializer,NewsSerializer,NewsCounterSerializer
from dataCollector.model_interfaces import Model_Interfaces



class TestModelMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.topic = Topics_model.db_insert_one_topic("Test topic")

    @classmethod
    def tearDown(self):
        Topics_model.objects.filter(topic_name__icontains="test").delete()
        News_model.objects.filter(news_title__icontains="test").delete()


    def test_insert_topic(self):
        self.assertEqual("Test topic", self.topic.topic_name, msg="Topic name is wrong")

    def test_insert_duplicated_topic(self):
        d_topic = Topics_model.db_insert_one_topic("Test topic")
        #print("test2", "topic2 type",type(d_topic))
        self.assertIsNone(d_topic)

    def test_get_topic_name_by_id(self):
        id = self.topic.id
        name = self.topic.topic_name
        topic_check = Topics_model.db_get_one_topic_by_id(id)
        # self.assertIsNotNone(topic_check)
        self.assertEqual(name, topic_check.topic_name)


    def test_get_topic_name_by_unexist_id(self):
        id = 100
        name = self.topic.topic_name
        topic_check = Topics_model.db_get_one_topic_by_id(id)
        self.assertIsNone(topic_check)

    def test_get_topic_name(self):
        name = self.topic.topic_name
        topic_check = Topics_model.db_get_one_topic_by_name(name)
        self.assertEqual(name, topic_check.topic_name)

    def test_get_topic_unexist_name(self):
        name = "Test topic 0"
        topic_check = Topics_model.db_get_one_topic_by_name(name)
        self.assertIsNone(topic_check)

    def test_get_all_recent_hot_topics(self):
        today = datetime.date.today()
        topic_check = Topics_model.db_get_all_recent_hot_topics(today)
        self.assertIsNotNone(topic_check)

    def test_get_all_recent_hot_topics_failed(self):
        today = datetime.date(2000,1,1)
        topic_check = Topics_model.db_get_all_recent_hot_topics(today)
        self.assertEqual([],topic_check)

    def test_get_recent_hot_topics(self):
        topic_check = Topics_model.db_get_recent_hot_topics()
        self.assertEqual([],topic_check)


    def test_insert_news(self):
        name = "test suitcase"
        Topics_model.db_insert_one_topic(name)
        topic_obj = Topics_model.db_get_one_topic_by_name(name)
        c_date =  timezone.now()
        News_model.db_insert_one_news(_title="test news title", _news_date=c_date, _summary="testing_news_summary_16",
                                      _news_url="wwww.google", _topic=topic_obj,
                                      _image_url="https://pbs.twimg.com/profile_images/626307178563960833/lKjVudoW.jpg")


    def test_count_ori_news(self):
        count = Ori_News_model.objects.all().filter(news_topic=1).order_by('news_date')\
            .extra({'news_date' : "date(news_date)"})\
            .values('news_topic','news_date')\
            .annotate(news_counter=Count('id'))
        list_count = list(count)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        list_days = [today - datetime.timedelta(days=x) for x in range(7, 0, -1)]
        list_new_count = []
        for day in list_days:
            obj = [x for x in list_count if x.get('news_date') == day]
            if len(obj) == 0:
                list_new_count.append({'news_topic': 1, 'news_counter': 0, 'news_date': day})
            else:
                list_new_count = list_new_count + obj
        obj = [x for x in list_count if x.get('news_date') == yesterday]
        print(list_days)
        print(list_new_count)
    # #
    #
    # def test_ori_news(self):
    #     name = "test suitcase"
    #     Topics_model.db_insert_one_topic(name)
    #     topic_obj = Topics_model.db_get_one_topic_by_name(name)
    #     current_date = timezone.now()
    #     news_url = "https://www.google.ie/"
    #     img_url = "http://lorempixel.com/400/250/"
    #     news_date = current_date - timedelta(days=1)
    #     news_title = 'test news title'
    #     summary = 'testing_news_summary'
    #     Ori_News_model.db_insert_one_news(news_title, news_date, summary, news_url, topic_obj, img_url)


    # def test_update_today(self):
    #     topic_list = Topics_model.objects.filter(latest_update_time__date=datetime.date.today())
    #     print(topic_list)



if __name__ == '__main__':
    unittest.main(verbosity=2)
