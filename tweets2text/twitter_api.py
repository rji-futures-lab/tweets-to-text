# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from TwitterAPI import TwitterAPI


def get_api():
    """
    Get an authenticated connection to Twitter's API.

    Return a `TwitterAPI` instance.
    """
    twitter_api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    return twitter_api
