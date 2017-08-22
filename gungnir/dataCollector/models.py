###########################################################
#     Create models for UCD-project's databases:
#         Author: Wenrui Shen 15210671, Hong Su 15211605
#         Date:     2017-06-17
#        Version: 1.3
#        Description:    Tables Definition;
#                        1st layer interfaces;
###########################################################
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import validate_comma_separated_integer_list
from django.db.utils import IntegrityError
import logging
from django.db.models import Count


logger = logging.getLogger('dataCollector')

# News source website
class Medium_model(models.Model):
    # id: default auto-incrementing Primary Key.
    media_name = models.CharField(max_length=24, unique=True)  # default: not null, not blank

    # media_logo_path = ImageField
    def __str__(self):
        return self.media_name

# Topics' data structure
class Topics_model(models.Model):
    # id: default auto-incrementing Primary Key.
    topic_name = models.CharField(max_length=200, unique=True)  # default: not null, not blank
    # Automatically recorded.
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    # Manually Input date.
    oldest_news_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # Updated each time after calling save().
    latest_news_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    # Whenever the topic is hot today, current system time is recorded.
    recent_hot_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # When news are inserted, current system time is recorted.
    latest_update_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # Record last time insert news into Filtered_news_DB.
    latest_filter_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # Record last news date which has been clustered
    latest_cluster_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.topic_name

    # 4.1.2.1: Insert one new topic.
    def db_insert_one_topic(name):
        try:
            topic, created = Topics_model.objects.get_or_create(topic_name=name)
            if created:
                #topic.recent_hot_date = datetime.datetime.now()
                topic.recent_hot_date = timezone.now()
                topic.save()
                return topic
            elif created is False:
                #logger.debug("[" + name + "] existed before.")
                return None
        except IntegrityError as uniqueError:
            logger.error("DB IntegrityError db_insert_one_topic failed: " + str(uniqueError))
            return None
        except Exception as e:
            logger.error("db_insert_one_topic failed: " + str(e))
            return None

    # 4.1.2.2: Select single topic info by id.
    def db_get_one_topic_by_id(topic_id):
        try:
            topic = Topics_model.objects.get(id=topic_id)
        except Exception as e:
            logger.error("DB DoesNotExist db_get_one_topic_by_id failed: " + str(e))
            topic = None
        return topic

    # 4.1.2.3: Select single topic info by name.
    def db_get_one_topic_by_name(name):
        try:
            topic = Topics_model.objects.get(topic_name=name)
        except Exception as e:
            logger.error("DB DoesNotExist db_get_one_topic_by_name failed: " + str(e))
            topic = None
        return topic


    # 4.1.2.4.1 Select all topics without limitation.
    def db_get_all_topics():
        topics_list = []
        try:
            queryset = Topics_model.objects.all()
            if queryset is not None:
                topic_list = list(queryset)
                return topic_list
            else:
                logger.info("No topic: db_get_all_topics")
                return None
        except Exception as e:
            logger.error("db_get_all_topics failed: " + str(e))
            return None

    # 4.1.2.4.2: Get hot topics at certain date
    def db_get_all_recent_hot_topics(input_date):
        topic_list = []
        try:
            #queryset = Topics_model.
            queryset = Topics_model.objects.all().filter(recent_hot_date__contains = input_date)
            if queryset is not None:
                topic_list = list(queryset)
            else:
                logger.info("No hot topic: db_get_all_recent_hot_topics")
                topic_list = None
        except Exception as e:
            logger.error("db_get_all_recent_hot_topics failed: " + str(e))
            topic_list = None
        return topic_list

    # 4.1.2.4.3 Select Some topics created before one date
    def db_get_all_topics_created_before_date(input_date):
        topic_list = []
        try:
            queryset = Topics_model.objects.all().filter(create_date__lte = input_date)
            if queryset is not None:
                topic_list = list(queryset)
                #logger.debug(topic_list)
            else:
                logger.debug(" No histroy topic earier than iuput date")
        except Exception as e:
            logger.error("db_get_all_topics_created_before_date failed: " + str(e))
            topic_list = None
        return topic_list

    # 4.1.2.4.4: Get recent hot topics without input date.
    def db_get_recent_hot_topics():
        try:
            #recent_date = Topics_model.objects.latest('recent_hot_date').recent_hot_date.date()
            #queryset = Topics_model.objects.filter(recent_hot_date__date = recent_date).order_by('-recent_hot_date')
            queryset = Topics_model.objects.all().order_by('-recent_hot_date')#.filter(latest_update_time=None)
            if queryset is not None:
                return queryset
            else:
                logger.info("No hot topic: db_get_recent_hot_topics")
                return None
        except Exception as e:
            logger.error("db_get_recent_hot_topics failed: " + str(e))
            return None

    # 4.1.2.4.5: Get recent hot topics without input date.
    def db_get_recent_hot_topics_rest():
        try:
            queryset = Topics_model.objects.all().exclude(latest_filter_time=None).order_by('-recent_hot_date')
            if queryset is not None:
                return queryset
            else:
                logger.info("No hot topic: db_get_recent_hot_topics_rest")
                return None
        except Exception as e:
            logger.error("db_get_recent_hot_topics_rest failed: " + str(e))
            return None

    # 4.1.2.4.6: Get N recent hot topics descendingly
    def db_get_n_recent_hot_topics_rest(topics_num, topics_start):
        try:
            queryset = Topics_model.objects.all().exclude(latest_filter_time=None).order_by('-recent_hot_date')
            if queryset is not None:
                if int(topics_start) >= len(queryset):
                    return None
                topic_set = queryset[int(topics_start): min(int(topics_start) + int(topics_num), len(queryset))]
                if len(topic_set) > 0:
                    return topic_set
                else:
                    return None
            else:
                logger.info("No hot topic: db_get_n_recent_hot_topics_rest")
                return None
        except Exception as e:
            logger.error("db_get_n_recent_hot_topics_rest failed: " + str(e))
            return None

    # 4.1.2.5:  Delete all topics without any news.
    def db_delete_all_topics_without_news():
        Topics_model.objects.filter(latest_update_time=None).delete()

    # 4.1.2.6: Update single topic info.
    def db_update_one_topic(topic):
        try:
            if type(topic) is Topics_model:
                topic.save()
                return topic
            else:
                return None
        except Exception as e:
            logger.error("db_update_one_topic failed: " + str(e))
            return None

    # 4.1.2.7: Update recent_hot_date
    def db_update_recent_hot_date(self):
        try:
            #self.recent_hot_date = datetime.datetime.now()
            self.recent_hot_date = timezone.now()
        except Exception as e:
            logger.error("db_update_recent_hot_date failed: " + str(e))
        return self

    def db_update_latest_cluster_time(topic_id, _latest_cluster_time):
        try:
            topic = Topics_model.objects.get(id=topic_id)
            if topic is not None:
                topic.latest_cluster_time = _latest_cluster_time
                topic.save()
            return topic
        except Exception as e:
            logger.error("db_update_latest_cluster_time failed: " + str(e))
            return None

    # Search topics with input info
    def db_search_topics(inputValue):
        return Topics_model.objects.filter(topic_name__icontains=inputValue)

    # Today Update/ update attribute latest_update_time
    def db_today_updated_topics():
        return Topics_model.objects.filter(latest_update_time__date=datetime.date.today())

# The model with attributes without other customized interfaces
# The model will be inherited
class Base_News_model(models.Model):
    # id: default auto-incrementing Primary Key.
    # default: not null, not blank
    news_title = models.CharField(max_length=200)
    # Manually Input date.
    news_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    # Store large text file.
    news_summarize = models.TextField(null=True, blank=True)
    news_content = models.TextField(null=True, blank=True)
    news_topic = models.ForeignKey(Topics_model, on_delete=models.CASCADE)
    media_id = models.ForeignKey(Medium_model, on_delete=models.CASCADE, null=True, blank=True)
    news_url = models.URLField(max_length=200, unique=True)
    image_url = models.URLField(max_length=200, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.news_title


# The model to store the news that scratches from news source website
class Ori_News_model(Base_News_model):
    # 4.1.3.1 insert one news
    def db_insert_one_news(_title, _news_date, _content, _summary, _news_url, _topic, _image_url):
        try:
            news = Ori_News_model(news_title=_title, news_date=_news_date, news_content=_content, news_summarize=_summary, news_url=_news_url,
                              news_topic=_topic, image_url=_image_url)
            news.save()
        except IntegrityError as uniqueError:
            logger.debug("DB IntegrityError db_insert_one_news failed: " + str(uniqueError))
            news = None
        except Exception as e:
            logger.error("db_insert_one_news failed: " + str(e))
            news = None
        return news

    # 4.1.3.2 select one article by id
    def db_get_one_news(news_id):
        try:
            news = Ori_News_model.objects.get(id=news_id)
        except Exception as e:
            logger.error("DB DoesNotExist db_get_one_news failed: " + str(e))
            news = None
        return news

    # 4.1.3.3 delete one article by id
    def db_delete_one_news(news_id):
        try:
            news = Ori_News_model.objects.get(id=news_id)
            if news is not None:
                news.delete()
                return 1
            else:
                return 0
        except Exception as e:
            logger.error("db_delete_one_news failed: " + str(e))
            return -1

    # 4.1.3.4 get news by topic id
    def db_get_news_by_topic_id(topic_id):
        try:
            topic = Topics_model.db_get_one_topic_by_id(topic_id)
            if topic is not None:
                queryset = Ori_News_model.objects.all().filter(news_topic=topic).order_by('-news_date')
                return queryset
            else:
                logger.info(" NO such Topic: db_get_news_by_topic_id")
                return None
        except Exception as e:
            logger.error("db_get_news_by_topic_id failed: " + str(e))
            return None
    # count the news for one topic that stores into DB daily
    def db_count_news_per_day(topic_id):
        try:
            topic = Topics_model.db_get_one_topic_by_id(topic_id)
            if topic is not None:
                queryset = Ori_News_model.objects.all().filter(news_topic=topic_id).order_by('news_date')\
                    .extra({'news_date' : "date(news_date)"})\
                    .values('news_topic','news_date')\
                    .annotate(news_counter=Count('id'))
                return queryset
            else:
                logger.info(" NO such Topic: db_get_news_by_topic_id")
                return None
        except Exception as e:
            logger.error("db_get_news_by_topic_id failed: " + str(e))
            return None

# The news model which shows the processed news
# Show to users
class News_model(Base_News_model):
    # 4.1.3.1 insert one news
    def db_insert_one_news(_title, _news_date, _summary, _news_url, _topic, _image_url):
        try:
            news = News_model(news_title=_title, news_date=_news_date, news_summarize=_summary, news_url=_news_url,
                              news_topic=_topic, image_url=_image_url)
            news.save()
        except IntegrityError as uniqueError:
            logger.debug("DB IntegrityError db_insert_one_news failed: " + str(uniqueError))
            news = None
        except Exception as e:
            logger.error("db_insert_one_news failed: " + str(e))
            news = None
        return news

    # 4.1.3.2 select one article by id
    def db_get_one_news(news_id):
        try:
            news = News_model.objects.get(id=news_id)
        except Exception as e:
            logger.error("DB DoesNotExist db_get_one_news failed: " + str(e))
            news = None
        return news

    # 4.1.3.3 delete one article by id
    def db_delete_one_news(news_id):
        try:
            news = News_model.objects.get(id=news_id)
            if news is not None:
                news.delete()
                return 1
            else:
                return 0
        except Exception as e:
            logger.error("db_delete_one_news failed: " + str(e))
            return -1

    # 4.1.3.4 get news by topic id
    def db_get_news_by_topic_id(topic_id):
        try:
            topic = Topics_model.db_get_one_topic_by_id(topic_id)
            if topic is not None:
                queryset = News_model.objects.all().filter(news_topic=topic).order_by('-news_date')
                return queryset
            else:
                logger.info(" NO such Topic: db_get_news_by_topic_id")
                return None
        except Exception as e:
            logger.error("db_get_news_by_topic_id failed: " + str(e))
            return None
