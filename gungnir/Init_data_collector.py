import django
import sys
import logging

django.setup()

from dataCollector.tasks import init_flow

logger = logging.getLogger('dataCollector')

logger.info("\n##############################################################\n" + "\tNow start init data collecting process:\n")

init_flow()

logger.info("\n\tInit data collecting period is over!\n" + "##############################################################\n")
