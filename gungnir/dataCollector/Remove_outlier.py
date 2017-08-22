import numpy as np
import logging

logger = logging.getLogger('dataCollector')

class R_outlier:
    def Remove_cluster_one(self, k_means_labels, k_value, centroids, sample_number):
        try:
            number_dic = {}
            for label in range(0, k_value):
                number_dic[label] = sum(k_means_labels == label)
            list_1 = sorted(number_dic.items(), key=lambda item: item[1], reverse=True)
            Remove_label = []
            dynamic_num_threshold = max(1, min((sample_number/k_value**2),10))
            logger.debug("Cluster num:" + str([cluster_num[1] for cluster_num in list_1]) + \
                         ",\t threshold:" + str(dynamic_num_threshold))
            for x in list_1:
                if x[1] <= dynamic_num_threshold:
                    Remove_label.append(x[0])
                    logger.debug("Remove cluster:" + str(x[0]) + ",\t num:" + str(x[1]))
            final_centroids = np.delete(centroids, Remove_label, axis=0)
            return final_centroids
        except Exception as e:
            logger.error("Remove_cluster_one" + str(e))
            return centroids

    def Remove_outlier_simi(self, cos_list):
        try:
            sum_cos = {}
            cos_index = 0
            for x in cos_list:
                sum_cos[cos_index] = sum(x) - 1
                cos_index = cos_index + 1
            list_cos = sorted(sum_cos.items(), key=lambda item: item[1], reverse=True)
            sum_c = []
            Remove_label = []
            for x in list_cos:
                sum_c.append(x[1])
            discrete_cos_sim_threshold = max(np.mean(sum_c) * 0.6, 0.01)
            logger.debug("discrete_cos_sim_threshold:" + str(discrete_cos_sim_threshold) + ";\tsim_mean:" + str(list_cos))

            for sum_x in list_cos:
                if sum_x[1] < discrete_cos_sim_threshold:
                    Remove_label.append(sum_x[0])
            return Remove_label
        except Exception as e:
            logger.error("Remove_outlier_simi" + str(e))
            return None