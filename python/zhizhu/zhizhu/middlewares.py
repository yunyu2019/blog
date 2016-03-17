#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from zhizhu.settings import USER_AGENTS

class RandomUserAgentMiddleware(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            request.headers.setdefault('User-Agent', ua)
