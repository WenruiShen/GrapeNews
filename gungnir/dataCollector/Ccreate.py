# -*- coding: utf-8 -*-
"""
Created on Wed May 31 16:11:58 2017

@author: Ovenus
"""
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
import requests
from newspaper import Article 
import dataCollector.Ctime
import socket
from urllib.error import URLError, HTTPError
import time
from urllib.parse import urlparse
import codecs
import logging

logger = logging.getLogger('dataCollector')



class Medium:
    # extract_news V2.0
    def extract_newsV2(self, newsurl_list_ori, newsdate_list_ori, start_date):
        nyt_img_list = ['https://static01.nyt.com/images/icons/t_logo_291_black.png', 'https://static01.nyt.com/images/common/icons/t_wb_75.gif']
        news_content_list = []
        news_summary_list = []
        pub_date = []
        news_titles = []
        top_image = []
        links_list = []
        index = 0
        time_comp = dataCollector.Ctime.C_times()
        try:
            if newsurl_list_ori is not None:
                for link in newsurl_list_ori:
                    i = 0
                    if ((start_date is None) or (time_comp.Ctoday(newsdate_list_ori[index], start_date) == 1)):
                        news_DOC = Article(url=link)
                        news_DOC.download()
                        news_DOC.parse()
                        if news_DOC.top_image not in nyt_img_list:
                            news_content = news_DOC.text
                            news_content_list.append(news_content)
                            image = news_DOC.top_image
                            top_image.append(image)
                            news_pubtime = newsdate_list_ori[index]
                            pub_date.append(news_pubtime)
                            news_title = news_DOC.title
                            news_titles.append(news_title)
                            links_list.append(link)
                            news_DOC.nlp()
                            news_summary_list.append(news_DOC.summary)
                    index = index + 1
            return news_content_list, news_summary_list, pub_date, news_titles, links_list, top_image
        except Exception as e:
            logger.error("Medium.extract_newsV2 failed: " + str(e))
            return news_content_list, news_summary_list, pub_date, news_titles, links_list, top_image


class NYT(Medium):
    # generate url V1.0
    def create_NYTURL(self, num_page,search_q, bd):
        base = "http://api.nytimes.com/svc/search/v2/"
        b1 = "articlesearch.json?q="
        b_d = "&begin_date="
        page = "&page="
        key = "&api-key=d0bf06609528439b8bff9e868c97b1f2"
        url_q = b1 + search_q + b_d + str(bd) + page + str(num_page) + key
        url1 = urllib.parse.urljoin(base, url_q)
        arr = urlparse(url1)
        return urllib.parse.urlunparse((arr.scheme, arr.netloc, arr.path, arr.params, arr.query, arr.fragment))

    # generate url request V2.0
    def create_NYTURL_2(self, num_page,search_q, bd):
        base = "http://api.nytimes.com/svc/search/v2/articlesearch"
        response_format = ".json"
        key = "d0bf06609528439b8bff9e868c97b1f2"
        #r = None
        search_p = {"q":search_q, "api-key":key, "page":num_page, "begin_date":bd}
        try:
            r = requests.get(base+response_format, params = search_p)
            #time.sleep(0.15)
            #logger.debug(str(r.url))
            r.raise_for_status()
            return r
        except requests.RequestException as rex:
            logger.error("NYT.create_NYTURL_2 RequestException failed: " + str(rex))
            return None
        except Exception as e:
            logger.error("NYT.create_NYTURL_2 failed: " + str(e))
            return None

    def create_NYTURL_2_1(self, num_page, search_q):
        url_base = 'https://query.nytimes.com/svc/add/v1/sitesearch.json?sort=desc&fq=document_type%3A%22article%22&facet=true'
        search_p = {"q": search_q, "page": num_page}
        try:
            r = requests.get(url_base, params=search_p)
            # logger.debug(str(r.url))
            r.raise_for_status()
            return r
        except requests.RequestException as rex:
            logger.error("NYT.create_NYTURL_2 RequestException failed: " + str(rex))
            return None
        except Exception as e:
            logger.error("NYT.create_NYTURL_2 failed: " + str(e))
            return None

    # parse daily json response V1.0
    def parse_json(self, nyt_respone, lastes_date) :
        #NYT_Q = NYT_respone
        nyt_r = nyt_respone
        nyt_data = nyt_r.json()
        nyt_newsurl = []
        nyt_newsdate = []
        try:
            if (len(nyt_data["response"])!=0):
                nyt_articles = nyt_data["response"]["docs"]
                time_comp = dataCollector.Ctime.C_times()
                for article in nyt_articles:
                    if (time_comp.Ctoday((article['pub_date']),lastes_date) == 1):
                        nyt_newsurl.append(article['web_url'])
                        nyt_newsdate.append(article['pub_date'])
            return nyt_newsurl, nyt_newsdate
        except Exception as e:
            logger.error("NYT.parse_json failed: " + str(e))
            return None, None
    '''
    #  parse history json response V1.0
    def parse_past_json(self, nyt_respone) :
        #NYT_Q = NYT_url
        nyt_r = nyt_respone
        nyt_data = nyt_r.json()
        nyt_newsurl = []
        nyt_newsdate = []
        try:
            if (len(nyt_data["response"])!=0):
                nyt_articles = nyt_data["response"]["docs"]
                for article in nyt_articles:
                    nyt_newsurl.append(article['web_url'])
                    nyt_newsdate.append(article['pub_date'])
            return nyt_newsurl, nyt_newsdate
        except Exception as e:
            logger.error("NYT.parse_past_json failed: " + str(e))
            return nyt_newsurl, nyt_newsdate
    '''

class BBC(Medium):
    # generate url V1.0
    def create_URL(self, num_page,search_q):
        base = "http://www.bbc.co.uk/search/"
        b1 = "more?page="
        b2 = "&q="
        b3 = "&filter=news&suggid="
        url_q = b1 + str(num_page) + b2 + search_q + b3
        url1 = urllib.parse.urljoin(base, url_q)
        arr = urlparse(url1)
        return urllib.parse.urlunparse((arr.scheme, arr.netloc, arr.path, arr.params, arr.query, arr.fragment))

    # generate url request V2.0
    def create_URL_2(self, num_page,search_q):
        base = "http://www.bbc.co.uk/search/"
        b1 = "more?page="
        search_p = { "q":search_q, "filter":"news sport music","suggid":"" }
        #search_p = {"q": search_q, "suggid": ""}
        url = None
        try:
            r = requests.get(base+b1+str(num_page), params = search_p)
            r.raise_for_status()
        except requests.RequestException as rxt:
            logger.error("BBC.create_URL RequestException failed: " + str(rxt))
            return None
        except Exception as e:
            logger.error("BBC.create_URL failed: " + str(e))
            return None
        else:
            url = r.content
            return url

    # extract web content V1.0
    def extract_web(self, url):
        timeout = 2
        socket.setdefaulttimeout(timeout)
        html = None
        try:
            response = urllib.request.urlopen(url);# Response from the server
            html = response.read().decode('utf-8');# Return the binary string, and Decode it
            return html
        except HTTPError as e:
            logger.error("BBC.extract_web failed (The server couldn't fulfill the request): " + str(e.code))
            return None
        except URLError as e:
            logger.error("BBC.extract_web failed (We failed to reach a server): " + str(e.reason))
            return None
        except Exception as e:
            logger.error("BBC.extract_web failed: " + str(e))
            return None

    # parse html to get news url V1.0
    def analysis_html(self, content):
        link = []
        try:
            soup = BeautifulSoup(content,"lxml");# Build the object of BeautifulSoup
            for h1 in soup.find_all("h1",{"itemprop":"headline"}):
                for i in h1.find_all('a'): # According to the for loop to extraact all URL from given html content
                    url_list = i.get('href')
                    link.append(url_list)
            return link
        except AttributeError as e:
            logger.error("BBC.analysis_html failed: " + str(e))
            return None
        except Exception as e:
            logger.error("BBC.analysis_html failed: " + str(e))
            return None

    # parse html to get pub_time  V1.0
    def New_pubdata(self, content):
        date_list = []
        try:
            soup = BeautifulSoup(content,"lxml");# Build the object of BeautifulSoup
            for d1 in soup.find_all('aside',{"class":"flags top"}):
                for t1 in d1.find_all('time'):
                    time_list = t1.get('datetime')
                    date_list.append(time_list)
            return date_list
        except AttributeError as e:
            logger.error("BBC.New_pubdata failed: " + str(e))
            return date_list

    ## Combine publish date and news url V1.0
    def extract_pubtime_newsurl(self, content):
        C = dataCollector.Ctime.C_times()
        urllist = []
        timelist = []
        i = 1
        try:
            if content is not None:
                soup = BeautifulSoup(content, "lxml");  # Build the object of BeautifulSoup
                for h1 in soup.find_all("article"):
                    j = 0
                    for s2 in h1.find_all("aside", {"class": "flags top"}):
                        if len(s2.contents) == 1:
                            j = 1
                            break
                        temple1 = s2.contents[1].contents[3].contents[1]
                        time_list = temple1.get('datetime')
                        timelist.append(time_list)
                    if j == 0:
                        for s1 in h1.find_all("h1", {"itemprop": "headline"}):
                            temple = s1.contents[0]
                            urllist.append(temple.get("href"))
                    i = i + 1

            return urllist, timelist
        except Exception as e:
            logger.error("BBC.extract_pubtime_newsurl failed: " + str(e))
            return None, None


class ABC(Medium):
    # create url V1(not use yet)
    def create_URL(self, num_page, search_q):
        try:
            number = num_page * 15
            base = 'http://abcnews.go.com/search'
            search = {'searchtext': search_q, 'r': 'story'}
            data = urllib.parse.urlencode(search)
            url_ = base + '?' + data + '#' + str(number)
            return url_
        except Exception as e:
            logger.error("ABC.create_URL failed: " + str(e))
            return None
    # create abc search engine url
    def create_URL2(self, num_page, search_q):
        try:
            base = "http://abcnews.go.com/meta/javascript/loadmarkup?include=%2Fmeta%2Fsearch%2Fresults%3Fsearchtext%3D"
            base2 = "%26r%3Dstory%26offset%3D"
            base3 = "%26sort%3D"
            q = search_q
            fin_q = q.replace(" ", '%20')
            fin_q = fin_q.replace("'","%27")
            i = num_page * 15
            url_ = base + fin_q + base2 + str(i) + base3
            return url_
        except Exception as e:
            logger.error("ABC.create_URL2 failed: " + str(e))
            return None
    # get html response
    def extract_web(self, url):
        timeout = 2
        socket.setdefaulttimeout(timeout)
        html = None
        try:
            response = urllib.request.urlopen(url);# Response from the server
            html = response.read().decode('utf-8');# Return the binary string, and Decode it
            return html
        except HTTPError as e:
            logger.error("ABC.extract_web failed (The server couldn't fulfill the request): " + str(e.code))
            return None
        except URLError as e:
            logger.error("ABC.extract_web failed (We failed to reach a server): " + str(e.reason))
            return None
        except Exception as e:
            logger.error("ABC.extract_web failed: " + str(e))
            return None
    # extract news url V1
    def analysis_html(self, content):
        link = []
        try:
            nn = codecs.getdecoder("unicode_escape")(content)[0]
            fin_nn = nn.replace("\\", '')
            nn3 = codecs.getdecoder("unicode_escape")(fin_nn)[0]
            soup = BeautifulSoup(nn3, 'lxml');  # Build the object of BeautifulSoup
            for h1 in soup.find_all("a", {"class": "title"}):
                # logger.debug(str(h1))
                url_list = h1.get('href')
                #fin = url_list.replace("\\", '')
                link.append(url_list)
            return link
        except AttributeError as e:
            logger.error("ABC.analysis_html failed: " + str(e))
            return None
        except Exception as e:
            logger.error("ABC.analysis_html failed: " + str(e))
            return None
    # extract news publish date V1
    def extract_pubtime(self, content):
        C = dataCollector.Ctime.C_times()
        time_list = []
        try:
            nn = codecs.getdecoder("unicode_escape")(content)[0]
            fin_nn = nn.replace("\\", '')
            nn3 = codecs.getdecoder("unicode_escape")(fin_nn)[0]
            soup2 = BeautifulSoup(nn3, 'lxml');  # Build the object of BeautifulSoup
            for h1 in soup2.find_all("span", {"class": "date"}):
                #logger.debug(str(h1.text))
                sub_time = h1.text
                stamp = C.str_to_timestamp(sub_time)
                sub_time_zone = str(C.parse_timestamp(stamp))[0:11] + "00:00:00.000Z"
                time_list.append(sub_time_zone)
            return time_list
        except Exception as e:
            logger.error("ABC.extract_pubtime failed: " + str(e))
            return None
    ## Combine publish date and news url V1.0
    def extract_pubtime_newsurl(self, content):
        C = dataCollector.Ctime.C_times()
        urllist = []
        timelist = []
        try:
            nn = codecs.getdecoder("unicode_escape")(content)[0]
            fin_nn = nn.replace("\\", '')
            nn3 = codecs.getdecoder("unicode_escape")(fin_nn)[0]
            soup2 = BeautifulSoup(nn3, 'lxml');  # Build the object of BeautifulSoup
            ##for h1 in soup2.find_all([{"class": "result Story"},{"class": "result WireStory"}]):
            for h1 in soup2.find_all("div",class_ = [ "result Story", "result WireStory"]):
                #logger.debug(str(h1))
                for s1 in h1.find_all("a", {"class": "title"}):
                    # logger.debug(str(s1))
                    urllist.append(s1.get("href"))
                for s2 in h1.find_all("span", {"class": "date"}):
                    sub_time = s2.text
                    stamp = C.str_to_timestamp(sub_time)
                    sub_time_zone = str(C.parse_timestamp(stamp) + ".000Z")
                    timelist.append(sub_time_zone)
            return urllist, timelist
        except Exception as e:
            logger.error("ABC.extract_pubtime_newsurl failed: " + str(e))
            return None, None

class CNN(Medium):
    # get news from CNN API
    def create_URL2(self, num_page, search_q):
        base = "https://search.api.cnn.io/content?"
        b1 = "category=us,politics,world,opinion,health"
        q = search_q
        page_s = 10
        number = num_page
        number_ = (number - 1) * 10
        search_p = {"q": q, "size": page_s, "type": "article", "page": number, "from": number_}
        try:
            r = requests.get(base + b1, params=search_p)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            logger.error("CNN.create_URL2 failed (RequestException): " + str(e))
        except Exception as e:
            logger.error("CNN.create_URL2 failed: " + str(e))
            return None

    def parse_json_CNN(self, cnn_respone, lastes_date):
        url_list = []
        time_list = []
        try:
            cnn_r = cnn_respone
            cnn_data = cnn_r.json()
            #logger.debug(str(cnn_data))
            if (len(cnn_data["result"]) != 0):
                time_comp = dataCollector.Ctime.C_times()
                articles_url = cnn_data["result"]
                # logger.debug(str(articles_url))
                for article in articles_url:
                    if (time_comp.Ctoday((article['firstPublishDate']), lastes_date) == 1):
                        url_list.append(article["url"])
                        time_list.append(article["firstPublishDate"])
            return url_list, time_list
        except Exception as e:
            logger.error("CNN.parse_json_CNN failed: " + str(e))
            return None, None