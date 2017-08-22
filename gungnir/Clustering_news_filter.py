import django
import sys
import logging

django.setup()

from dataCollector.tasks import cluster_test_flow, latest_cluster_time_mark_clean, cluster_flow, all_latest_cluster_time_mark_clean

logger = logging.getLogger('dataCollector')

logger.info("\n\tNow start cluster_test_flow:\n")

all_latest_cluster_time_mark_clean()
cluster_flow()

#latest_cluster_time_mark_clean()
#cluster_test_flow()

logger.info("\n\tcluster_test_flow is over!\n")
