# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 13:58:35 2017

@author: Ovenus
"""

import dataCollector.Past_news

c =dataCollector.Past_news.ALL_news()
news, times, titles, url = c.Past('trump',1, 20170530)


b = dataCollector.Past_news.ALL_news()
Bnews, Btimes, Btitles, Burl = b.daily('trump trump',1,'2008-09-26T01:51:42.000Z')
