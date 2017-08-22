###############################################
#    Testing model.py and its interfaces.
#        Author:     Wenrui Shen 15210671 Hong Su 15211605
#        Date:        2017-06-06
#        Version:    1.2
#        Description:    Testing Topics_model & News_model: 1st layer API
###############################################
import django
django.setup()
import datetime
# inmport models from your model application
from dataCollector.models import Topics_model,News_model,Medium_model
from dataCollector.model_interfaces import Model_Interfaces

# test for Topic_model
# test 1 -- test 4.1.2.1
# Test Name: Insert one new topic
# Expect Output: topic's str
print("\ntest 1 -- test 4.1.2.1")
print("Test Name: Insert one new topic")
print("Expect Output: topic's id, name, date")
topic = Topics_model.db_insert_one_topic("Technology")
temp_id = topic.id
temp_name = topic.topic_name
print("Actual Output:")
print(topic.id)
print(topic.topic_name)
print(topic.create_date)
topic.delete()


Topics_model.db_insert_one_topic("Science")
Topics_model.db_insert_one_topic("Mathematic")
Topics_model.db_insert_one_topic("Trump election")
Topics_model.db_insert_one_topic("Presentent Putin")
Topics_model.db_insert_one_topic("ISIS")
Topics_model.db_insert_one_topic("Sourth China Sea")
Topics_model.db_insert_one_topic("North Korea Nuclear Weapon")

# test 2 -- test 4.1.2.1
# Test Name: Insert dupelicated topic
# Expect Output: [*] IntegrityError & None
print("\ntest 2 -- test 4.1.2.1")
print("Test Name: Insert dupelicated topic")
print("Expect Output: [*] IntegrityError & None")
print("Actual Output:")
topic = Topics_model.db_insert_one_topic("ISIS")
print(topic)



#if topic is not None:
#    topic.delete()
#print("All topics:")
#print(Topics_model.objects.all())


# test 3 -- test 4.1.2.2
# Test Name: Get one topic by its id
# Expect Output: topic's name
print("\ntest 3 -- test 4.1.2.2")
print("Test Name : Get one topic by its id")
print("Expect Output: topic's id & name")
id = 2
print("Actual Output:")
topic = Topics_model.db_get_one_topic_by_id(id)
if topic is not None:
    print(topic.id)
print(topic)

# test 4 -- test 4.1.2.2
# Test Name: Get one topic by not exist id
# Expect Output: [*] IntegrityError & None
print("\ntest 4 -- test 4.1.2.2")
print("Test Name : Get one topic by not exist id")
print("Expect Output: [*] DoesNotExist & None")
id = 1
print("Actual Output:")
topic = Topics_model.db_get_one_topic_by_id(id)
print(topic)

# test 5 -- test 4.1.2.3
# Test Name: Get one topic by its name
# Expect Output: topic's name
print("\ntest 5 -- test 4.1.2.3")
print("Test Name : Get one topic by its name")
print("Expect Output: topic's name & id")
print("Actual Output:")
name = "Science"
topic = Topics_model.db_get_one_topic_by_name(name)
print(topic.id)

# test 6 -- test 4.1.2.3
# Test Name: Get one topic by not exist name
# Expect Output: [*] IntegrityError & None
print("\ntest 6 -- test 4.1.2.3")
print("Test Name : Get one topic by not exist name")
print("Expect Output: [*] DoesNotExist & None")
print("Actual Output:")
name = "Technology"
topic = Topics_model.db_get_one_topic_by_name(name)
print(topic)

# test 7 -- test 4.1.2.4
# Test Name: successfully update
# Expect Output: topic's name
print("\ntest 7 -- test 4.1.2.4")
print("Test Name : successfully update")
print("Expect Output: topic's name-- Presentent Putin")
print("Actual Output:")
c_date= datetime.datetime.now()
name = "Presentent Putin"
topic = Topics_model.db_get_one_topic_by_name(name)
topic.latest_news_date = c_date
topic = Topics_model.db_update_one_topic(topic)
print(topic)


# test 8 -- test 4.1.2.4
# Test Name: update failed
# Expect Output: None
print("\ntest 8 -- test 4.1.2.4")
print("Test Name : update failed")
print("Expect Output: None")
print("Actual Output")
topic = Topics_model.db_update_one_topic("")
print(topic)

# test for news model
# test 9 -- test 4.1.3.1
# Test Name: insert new news
# Expect Output: news's title
print("\ntest 9 -- test 4.1.3.1")
print("Test Name : insert new news ")
print("Expect Output: news's title -- new news")
#m = Medium_model(id=1, media_name="BBC")
#m.save()
#print(m)
print("Actual Output")
c_date = datetime.datetime.now()
topic = Topics_model.db_get_one_topic_by_id(2)
print(topic)
news = News_model.db_insert_one_news(_title="new news", _news_date=c_date, _summary="summary", _news_url="wwww.google", _topic=topic,_image_url="https://upload.wikimedia.org/wikipedia/en/e/e1/Fate_Coverart.png")
print(news)


# Insert more artificial news for testing.
name = "Science"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_01", _news_date=c_date, _summary="testing_news_summary_01",_news_url="wwww.google", _topic=topic,_image_url="https://ichef.bbci.co.uk/news/660/cpsprodpb/4CEF/production/_96559691_baby_composite.jpg")
    News_model.db_insert_one_news(_title="testing_news_02", _news_date=c_date, _summary="testing_news_summary_02",_news_url="wwww.google", _topic=topic,_image_url="http://i2.cdn.cnn.com/cnnnext/dam/assets/170615120947-warmbier-coma-split-restricted-large-169.jpg")
    News_model.db_insert_one_news(_title="testing_news_03", _news_date=c_date, _summary="testing_news_summary_03",_news_url="wwww.google", _topic=topic,_image_url="https://i.ytimg.com/vi/1mpc088gWeM/maxresdefault.jpg")

name = "Mathematic"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_04", _news_date=c_date, _summary="testing_news_summary_04", _news_url="wwww.google", _topic=topic,_image_url="https://images-na.ssl-images-amazon.com/images/I/61%2BuiCo%2BkkL._AC_SL230_.jpg")
    News_model.db_insert_one_news(_title="testing_news_05", _news_date=c_date, _summary="testing_news_summary_05", _news_url="wwww.google", _topic=topic,_image_url="http://cdn3.dualshockers.com/wp-content/uploads/2016/03/Fate_Estella-14.jpg")
    News_model.db_insert_one_news(_title="testing_news_06", _news_date=c_date, _summary="testing_news_summary_06", _news_url="wwww.google", _topic=topic,_image_url="http://gematsu.com/wp-content/uploads/2016/07/Fate-Extella_07-14-16_004.jpg")

name = "Trump election"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_07", _news_date=c_date, _summary="testing_news_summary_07",  _news_url="wwww.google", _topic=topic,_image_url="http://diarynote.jp/data/blogs/l/20091009/88951_200910092126296703_2.jpg")
    News_model.db_insert_one_news(_title="testing_news_08", _news_date=c_date, _summary="testing_news_summary_08",  _news_url="wwww.google", _topic=topic,_image_url="")
    News_model.db_insert_one_news(_title="testing_news_09", _news_date=c_date, _summary="testing_news_summary_09",  _news_url="wwww.google", _topic=topic,_image_url="")

name = "Presentent Putin"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_10", _news_date=c_date, _summary="testing_news_summary_10",  _news_url="wwww.google", _topic=topic,_image_url="https://pbs.twimg.com/profile_images/849605737617608704/tmHHKh7f.jpg")
    News_model.db_insert_one_news(_title="testing_news_11", _news_date=c_date, _summary="testing_news_summary_11",  _news_url="wwww.google", _topic=topic,_image_url="https://pbs.twimg.com/profile_images/848188127462031361/LR9bGs9q.jpg")
    News_model.db_insert_one_news(_title="testing_news_12", _news_date=c_date, _summary="testing_news_summary_12",  _news_url="wwww.google", _topic=topic,_image_url="http://31.media.tumblr.com/32ea99714e7296c9136528576c7f72ba/tumblr_n9dwkjiRSk1rxzudco3_250.gif")

name = "ISIS"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_13", _news_date=c_date, _summary="testing_news_summary_13", _news_url="wwww.google", _topic=topic,_image_url="http://post.phinf.naver.net/MjAxNzAzMzBfOTYg/MDAxNDkwODYxOTA2NDI3.SdGmtUYTHipMdejOt6VGPYVqogQbLzXQYwohHIv-Z4Yg.sSJXwpyDvcIv53ZAls5zh0EJ_ZNVJNFy2aJQsKiyct4g.JPEG/fate-stay-night-ubw-rin.jpg?type=w1200")
    News_model.db_insert_one_news(_title="testing_news_14", _news_date=c_date, _summary="testing_news_summary_14", _news_url="wwww.google", _topic=topic,_image_url="https://upload.wikimedia.org/wikipedia/en/e/e1/Fate_Coverart.png")
    News_model.db_insert_one_news(_title="testing_news_15", _news_date=c_date, _summary="testing_news_summary_15", _news_url="wwww.google", _topic=topic,_image_url="")

name = "Sourth China Sea"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_16", _news_date=c_date, _summary="testing_news_summary_16", _news_url="wwww.google", _topic=topic,_image_url="https://pbs.twimg.com/profile_images/626307178563960833/lKjVudoW.jpg")
    News_model.db_insert_one_news(_title="testing_news_17", _news_date=c_date, _summary="testing_news_summary_17", _news_url="wwww.google", _topic=topic,_image_url="")
    News_model.db_insert_one_news(_title="testing_news_18", _news_date=c_date, _summary="testing_news_summary_18", _news_url="wwww.google", _topic=topic,_image_url="https://pbs.twimg.com/profile_images/848188127462031361/LR9bGs9q.jpg")

name = "North Korea Nuclear Weapon"
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    News_model.db_insert_one_news(_title="testing_news_19", _news_date=c_date, _summary="testing_news_summary_19", _news_url="wwww.google", _topic=topic,_image_url="https://pbs.twimg.com/profile_images/849605737617608704/tmHHKh7f.jpg")
    News_model.db_insert_one_news(_title="testing_news_20", _news_date=c_date, _summary="testing_news_summary_20", _news_url="wwww.google", _topic=topic,_image_url="https://upload.wikimedia.org/wikipedia/en/e/e1/Fate_Coverart.png")
    News_model.db_insert_one_news(_title="testing_news_21", _news_date=c_date, _summary="testing_news_summary_21", _news_url="wwww.google", _topic=topic,_image_url="")


# test 10 -- test 4.1.3.1
# Test Name: insert news failed
# Expect Output: None
print("\ntest 10 -- test 4.1.3.1")
print("Test Name : insert news failed")
print("Expect Output: None")
print("Actual Output:")
news = News_model.db_insert_one_news(_title="new news", _news_date=c_date, _summary="summary", _news_url="wwww.google", _topic=2,_image_url="")
print(news)


# test 11 -- test 4.1.3.2
# Test Name: Selecet one article by its id
# Expect Output: news's id --1
print("\ntest 11 -- test 4.1.3.2")
print("Test Name : Selecet one article by its id ")
print("Expect Output: news's id --100000")
print("Actual Output:")
news = News_model.db_get_one_news(100000)
if news is not None:
    print(news.id)


# test 12 -- test 4.1.3.2
# Test Name: Select one article from unexist id
# Expect Output: [*] DoesNotExist & None
print("\ntest 12 -- test 4.1.3.2")
print("Test Name : Select one article from unexist id ")
print("Expect Output: [*] DoesNotExist & None")
print("Actual Output:")
news = News_model.db_get_one_news(2)
print(news)


# test 13 -- test 4.1.3.3
# Test Name: delete one article by id
# Expect Output: 1
print("\ntest 13 -- test 4.1.3.3")
print("Test Name : delete one article by id ")
print("Expect Output: 1")
print("Actual Output:")
flag = News_model.db_delete_one_news(1)
print(flag)

# test 14 -- test 4.1.3.3
# Test Name: delete one article by id which is not existing
# Expect Output: -1
print("\ntest 14 -- test 4.1.3.3")
print("Test Name : delete one article by id which is not existing ")
print("Expect Output: -1")
print("Actual Output:")
flag = News_model.db_delete_one_news(1)
print(flag)

# test-15.1, 4.2.1.6.1 Get recent hot topic:
print("\ntest 15.1 -- test 4.2.1.6.1")
print("Test Name : Get recent hot topic:")
print("Expect Output: Set of hot topics")
print("Actual Output:")
topics_set = Model_Interfaces.db2_get_recent_hot_topic()
print(topics_set)

# test-15.2, 4.2.1.6.2 Get top n recent hot topic:
print("\ntest 15.2 -- test 4.2.1.6.2")
print("Test Name : Get top n recent hot topic:")
print("Expect Output: N Set of hot topics")
print("Actual Output:")
topics_set = Model_Interfaces.db2_get_n_recent_hot_topic(10, 20)
print(topics_set)

# test-16, 4.2.2.2 Get some news under one certain topic:
print("\ntest 16 -- test 4.2.2.2")
print("Test Name : Get some news under one certain topic:")
print("Expect Output: Set of news under one topic")
print("Actual Output:")
name = "Science"
print("Topic_name:" + name)
topic = Topics_model.db_get_one_topic_by_name(name)
if topic is not None:
    news_set = Model_Interfaces.db2_get_news_of_one_topic(topic.id)
    print(news_set)

print("\n=========== ALL Models List =================")
print(Topics_model.objects.all())
print(News_model.objects.all())