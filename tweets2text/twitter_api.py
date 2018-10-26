# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize a connection to Twitter."""
import os
from flask import g
from TwitterAPI import TwitterAPI


def get_api():
    """
    Get an authenticated connection to Twitter's API.

    Add to application content, g.twitter_api, if missing.

    Return a `TwitterAPI` instance.
    """
    if 'twitter_api' not in g:
        g.twitter_api = TwitterAPI(
            os.getenv('TWITTER_CONSUMER_KEY'),
            os.getenv('TWITTER_CONSUMER_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    return g.twitter_api
