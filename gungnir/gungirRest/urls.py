from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from gungirRest import views
from rest_framework import routers

router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'topic', views.TopicViewSet, 'Topics_model')

urlpatterns = [
    url(r'^topics_latest/(?P<topics_num>[0-9]+)-(?P<topics_start>[0-9]+)/$', views.Topics_Latest_N.as_view()),
    url(r'^topic/(?P<topic_id>[0-9]+)/news/$', views.TopicNews.as_view()),
    url(r'^topic/(?P<topic_id>[0-9]+)/news_latest/(?P<news_num>[0-9]+)/$', views.TopicNews_Latest_N.as_view()),
    url(r'^topic/search/(?P<search_value>.+)/$', views.TopicSearch.as_view()),
    url(r'^topic/count/(?P<topic_id>[0-9]+)/$', views.NewCounter.as_view()),
    url(r'^topic/update/$', views.TopicUpdateToday.as_view()),
    url(r'', include(router.urls))  ,
    # url(r'^topics/$', views.TopicsList.as_view()),
    #url(r'^login/(?P<user_name>[0-9]+)/$', views.User_Login.as_view()),
    #url(r'^user/(?P<user_id>[0-9]+)/$', views.UserInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)