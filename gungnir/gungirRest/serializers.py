###########################################################
#		Serialization for DATA_COLLECTOR_APP_02:
# 		Author: Wenrui Shen 15210671
# 		Date: 	2017-06-19
#		Version: 1.1
#		Description:	Model Serialization;
###########################################################
from rest_framework import serializers
from dataCollector.models import Topics_model,News_model,Medium_model

class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics_model
        fields = ('id', 
        		'topic_name', 
        		'create_date',
        		'oldest_news_date', 
        		'latest_news_date', 
        		'recent_hot_date',
        		'latest_update_time')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News_model
        fields = ('id', 
        		'news_title', 
        		'news_date',
        		'news_summarize', 
        		'news_topic', 
        		'media_id',
        		'news_url',
        		'image_url')

class NewsCounterSerializer(serializers.Serializer):
	news_topic = serializers.IntegerField()
	news_counter = serializers.IntegerField()
	news_date = serializers.DateField()