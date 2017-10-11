# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:43:41 2017

@author: Ovenus
"""

import datetime, dateutil.parser
import time
import logging

logger = logging.getLogger('dataCollector')


class C_times:
    # Identify the sequence between to datetime
    def Ctoday(self, times, last_time):
        try:
            latest = last_time
            now = times
            d1 = dateutil.parser.parse(latest)
            d2 = dateutil.parser.parse(now)
            R_N = datetime.date.today()
            if d2 > d1 and d2.date() <= R_N:
                return 1
        except Exception as e:
            logger.error("Can not compare time, C_times.Ctoday failed: " + str(e))
            return 0

    # Tranlate str to timestamp
    def str_to_timestamp(self, time_str):
        try:
            dt = dateutil.parser.parse(time_str)
            return time.mktime(dt.timetuple())
        except Exception as e:
            logger.error("C_times.str_to_timestamp: " + str(e))
            return None

    # According to time stamp generate useful datetime form
    def parse_timestamp(self, timestamp):
        try:
            timeArray = time.localtime(timestamp)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            return otherStyleTime
        except Exception as e:
            logger.error("C_times.parse_timestamp: " + str(e))
            return None