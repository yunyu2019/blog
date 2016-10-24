#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from zhihu.settings import USER_AGENT

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT)
        if ua:
            request.headers.setdefault('User-Agent', ua)