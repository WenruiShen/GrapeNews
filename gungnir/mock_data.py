import django
django.setup()
from django.utils import timezone
from dataCollector.models import Topics_model,News_model,Medium_model,Ori_News_model
from dataCollector.model_interfaces import Model_Interfaces
from datetime import timedelta
from random import randint

topic_name = ["Science", "Mathematic", "Trump election", "Presentent Putin", "ISIS", "Sourth China Sea",
              "North Korea Nuclear Weapon", "Turkish March for Justice", "Trump Putin meeting", "Cyberattacks on Ukraine",
              "Wimbledon 2017", "Nobel peace prize", "Amazon Echo", "Jaguar reveals E-peace", "Mayo Clinic", "Moon Express",
              "Janet Yellen", "National Economic Council", "Airbnb reservation", "Battle of Mosul", "Monkey selfie", "Wildfires in Europe"]

def generate_topics(names):
    Topics_model.db_insert_one_topic(names)


def generate_news(topic):
    topic_obj = Topics_model.db_get_one_topic_by_name(topic)
    news_date = timezone.now()
    news_url = "https://www.google.ie/"
    img_url = "http://lorempixel.com/400/250/"
    if topic_obj is not None:
        for i in range(3):
            news_title = topic + " - news - " + str(i)
            summary = topic + " - news summary - " + str(i)
            News_model.db_insert_one_news(news_title, news_date, summary, news_url, topic_obj, img_url)


for name in topic_name:
    Topics_model.db_insert_one_topic(name)
    generate_news(name)


def generate_ori_news(topic):
    topic_obj = Topics_model.db_get_one_topic_by_name(topic)
    current_date = timezone.now()
    news_url = "https://www.google.ie/"
    img_url = "http://lorempixel.com/400/250/"
    if topic_obj is not None:
        for day in range(1, 5):
            news_date = current_date - timedelta(days=day)
            for i in range(randint(0, 6)):
                news_title = topic + " - day - " + str(day) + " - news - " + str(i)
                summary = topic + " - day - "+ str(day) + " - news summary - " + str(i)
                Ori_News_model.db_insert_one_news(news_title, news_date, summary, news_url, topic_obj, img_url)


for name in topic_name:
    generate_ori_news(name)