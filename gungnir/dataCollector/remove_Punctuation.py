import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#import string
import logging

logger = logging.getLogger('dataCollector')

class Remove:
    # Remove sectional Punctuation from topic
    def removePunctuation(self, text):
        try:
            punctuation = '!,;:?"'
            text = re.sub(r'[{}]+'.format(punctuation), '', text)
            return text.strip()
        except Exception as e:
            logger.error("Remove.removePunctuation failed: " + str(e))
            return text

    # Remove stop words and some Punctuation from word
    def removestopword(self, text):
        try:
            stop_words = set(stopwords.words('english'))
            stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', 'this', 'the'])
            sentence = text
            words = word_tokenize(sentence)
            cleaned_text = filter(lambda x: x.lower() not in stop_words, words)
            a = ' '
            clean_topic = a.join(cleaned_text)
            return clean_topic
        except Exception as e:
            logger.error("Remove.removestopword failed: " + str(e))
            return text

