#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import random
import logging
from songs.settings import USER_AGENTS
from scrapy.downloadermiddlewares.retry import RetryMiddleware

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class MyRetryMiddleware(RetryMiddleware):
    def __init__(self,*a, **kw):
        super(MyRetryMiddleware, self).__init__(*a, **kw)
        logger=logging.getLogger('songs')
        formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
        logger.setLevel(logging.ERROR)
        handler=logging.FileHandler('/home/www/songs/error.log',mode='a',encoding='utf-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.err_logger=logger
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        if retries <= self.max_retry_times:
            self.err_logger.debug(u"Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries,'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            self.err_logger.error(u"Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
