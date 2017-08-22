###############################################
#        views.py for REST_APP_01.
#        Author:     Wenrui Shen 15210671 Hong Su 15211605
#        Date:        2017-06-19
#        Version:    1.0
#        Description:
###############################################
#from django.shortcuts import render

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework import viewsets

from dataCollector.models import Topics_model,News_model,Ori_News_model
from gungirRest.serializers import TopicsSerializer,NewsSerializer,NewsCounterSerializer
from dataCollector.model_interfaces import Model_Interfaces
import datetime
# class TopicsList(generics.ListCreateAPIView):
#     # Get top hottest topics.
#     queryset = Model_Interfaces.db2_get_recent_hot_topic()
#     serializer_class = TopicsSerializer
#
# class TopicDetail(generics.RetrieveAPIView):
#     queryset = Topics_model.objects.all()
#     serializer_class = TopicsSerializer

# api/topic/:id => list all topics or return specified topic
class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicsSerializer
    def get_queryset(self):
        hot_topics = Model_Interfaces.db2_get_recent_hot_topic_rest()
        return hot_topics if len(hot_topics) > 0 else None

# api/topics_latest/N1-N2 => return N topics order by id descending
class Topics_Latest_N(APIView):
    # Get top 'N' hottest topics.
    def get(self, request, topics_num, topics_start, format=None):
        n_topics = Model_Interfaces.db2_get_n_recent_hot_topic_rest(topics_num, topics_start)
        serializer = TopicsSerializer(n_topics, many=True)
        if len(serializer.data)>0:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

# api/topic/:id/news => return all news under specified topic
class TopicNews(APIView):
    # List one topics' News.
    def get(self, request, topic_id, format=None):
        news = Model_Interfaces.db2_get_filter_news_of_one_topic(topic_id)
        serializer = NewsSerializer(news, many=True)
        if len(serializer.data)>0:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

# api/topic/:id/news_latest/N => return N news under specified topic order by news_date
class TopicNews_Latest_N(APIView):
    # Get latested N news under a specified topic.
    def get(self, request, topic_id, news_num, format=None):
        #news = Model_Interfaces.db2_get_news_of_one_topic(topic_id)
        n_news = Model_Interfaces.db2_get_n_recent_news_under_one_topic(topic_id, news_num)
        serializer = NewsSerializer(n_news, many=True)
        if len(serializer.data)>0:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TopicSearch(APIView):
    def get(self, request, search_value, format=None):
        search_topics = Model_Interfaces.db2_topics_search(search_value)
        serializer = TopicsSerializer(search_topics, many=True)
        if len(serializer.data)>0:
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

class NewCounter(generics.ListAPIView):
    serializer_class = NewsCounterSerializer
    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        list_counter = list (Ori_News_model.db_count_news_per_day(topic_id))
        today = datetime.date.today()
        list_days = [today - datetime.timedelta(days=x) for x in range(7, 0, -1)]
        list_new_counter = []
        for day in list_days:
            obj = [x for x in list_counter if x.get('news_date') == day]
            if len(obj) == 0:
                list_new_counter.append({'news_topic': topic_id, 'news_counter': 0, 'news_date': day})
            else:
                list_new_counter = list_new_counter + obj
        return list_new_counter

class TopicUpdateToday(generics.ListAPIView):
    queryset = Topics_model.db_today_updated_topics()

    serializer_class = TopicsSerializer


# # api/topics_latest/N => return N topics order by id descending
# # class Topics_Latest_N(APIView):
# #     # Get top 'N' hottest topics.
# #     def get(self, request, topics_num, format=None):
# #         n_topics = Model_Interfaces.db2_get_n_recent_hot_topic(topics_num)
# #         serializer = TopicsSerializer(n_topics, many=True)
# #         if len(serializer.data)>0:
# #             return Response(serializer.data)
# #         return Response(status=status.HTTP_204_NO_CONTENT)