import urllib.request
import json
import bs4
import arrow
from urllib.error import URLError, HTTPError
import re
import dataCollector.remove_Punctuation
from bs4 import Tag, NavigableString
import logging

logger = logging.getLogger('dataCollector')

def get_date_n_day_before(n_days):
    n_days_hours = -24 * n_days
    day_n = arrow.now().replace(hours=n_days_hours).format('DD')
    day_n = day_n.replace("0", "", 1) if day_n.startswith("0") else day_n
    month_n = arrow.now().replace(hours=n_days_hours).format('MMMM')
    year_n = arrow.now().replace(hours=n_days_hours).format('YYYY')
    return year_n, month_n, day_n

def list_overlap(a, b):
    return bool(set(a) & set(b))

def ishypen(s):
    if "–" in s and (not any(char.isdigit() for char in s)):
        return True
    return False

def isapostrophe(s):
    if "'" in s and (not any(char.isdigit() for char in s)):
        return True
    return False

class topics:
    # Organize topics' usls.
    def url_organizer(year, month, day):
        url_head = url0 = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Portal%3ACurrent+events%2F"
        url_tail = "&rvprop=content&rvparse=1"
        url = url_head + str(year) + "+" + str(month) + "+" + str(day) + url_tail
        return url

    # get response from wikipedia Current event V2.0
    def get_response(self, N_day):
        # get today's date
        logger.info("Get hot Wiki topics [" + str(N_day) + "] days ago.")
        year, month, day = get_date_n_day_before(N_day)
        # generate dynamic url
        url = topics.url_organizer(year, month, day)
        try:
            raw_json_list = []
            response = urllib.request.urlopen(url)
            raw_json = response.read().decode("utf-8")
            raw_json_list.append(raw_json)
            return raw_json_list
        except HTTPError as e:
            logger.error("The server couldn't fulfill the request: " + str(e.code))
            return None
        except URLError as e:
            logger.error("We failed to reach a server: " + str(e.reason))
            return None

    # parse json to get topic V2.0
    def pares_raw_data(self, raw_json_list):
        try:
            topics = []
            for raw_json in raw_json_list:
                #logger.debug(raw_json)
                raw_data = json.loads(raw_json)
                remove = dataCollector.remove_Punctuation.Remove()
                pageid = list(raw_data["query"]["pages"].keys())[0]
                html = raw_data["query"]["pages"][pageid]["revisions"][0]["*"]
                #logger.debug(links)
                parser = bs4.BeautifulSoup(html,'html.parser')
                links = parser.find_all('a', title=True)
                for link in links:
                    title = link.text
                    if title is None:
                        continue
                    if len(title.split()) >= 2:
                        title = ''.join([i for i in title if not i.isdigit()]) #remove year
                        a1 = re.compile(r'\([^}]*\)')
                        re_title = a1.sub('', title)
                        f_title = remove.removePunctuation(re_title)
                        clean_title = remove.removestopword(f_title)
                        if clean_title not in topics:
                            topics.append(clean_title)
            return topics
        except Exception as e:
            logger.error("pares_raw_data() get topic from wiki error: " + str(e))
            return None

    # parse json to get topic V3.0
    def pares_raw_data_2(self, raw_json_list):
        try:
            topics = []
            clean_topics = []
            titles = []
            for raw_json in raw_json_list:
                raw_data = json.loads(raw_json)
                remove = dataCollector.remove_Punctuation.Remove()
                pageid = list(raw_data["query"]["pages"].keys())[0]
                html = raw_data["query"]["pages"][pageid]["revisions"][0]["*"]
                parser = bs4.BeautifulSoup(html,'html.parser')
                for b1 in parser.find_all('td', class_='description'):
                    for ul in b1.find_all('ul'):
                        for li in ul.find_all('li'):
                            if len(li.contents) > 0:
                                if getattr(li.contents[0], 'name', None) == 'a':
                                    titles.append(li.contents[0].text)
                for title in titles:
                    title_words = []
                    a1 = re.compile(r'\([^}]*\)') #remove string in brackets
                    re_title = a1.sub('', title)
                    clean_title = remove.removePunctuation(re_title)
                    #clean_title = remove.removestopword(f_title)
                    if clean_title is None:
                        continue
                    if len(clean_title.split()) >= 2:
                        for i in clean_title.split():
                            if i.isalpha() or ishypen(i) or isapostrophe(i) or not (i.isalpha() or i.isdigit()) and i.isalnum():
                                title_words.append(i)
                            topic = ' '.join(title_words)
                        if topic not in topics:
                            if len(topics) == 0:
                                topics.append(topic)
                                continue
                            clean_topic = remove.removestopword(topic)
                            if list_overlap(clean_topic.split(), topics[-1].split()) is False:
                                topics.append(topic)
                                clean_topics.append(clean_topic)
            #logger.debug(topics)
            return topics
        except Exception as e:
            logger.error("pares_raw_data_2() get topic from wiki error: " + str(e))
            return None
