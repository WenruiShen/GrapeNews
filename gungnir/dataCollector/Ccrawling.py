# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:53:17 2017

@author: Ovenus
"""
import newspaper
import logging

logger = logging.getLogger('dataCollector')

class Hot_topic:
    
    def extract_hot(self):
        self.hot = newspaper.hot()
        logger.debug("")
        return newspaper.hot()

def extract_hot2():
    Hot = newspaper.hot()
    logger.debug(str(Hot))
    return newspaper.hot()
    


