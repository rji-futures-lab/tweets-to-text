# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize an instance of the tweets2text app.
"""
import logging
from flask import Flask


__author__ = 'James Gordon'
__email__ = 'gordonj@rjionline.org'


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    from .commands import add_all as add_all_commands
    add_all_commands(app)

    from .views import index
    app.register_blueprint(index.bp, url_prefix='/')

    from .views.webhooks import twitter
    app.register_blueprint(
        twitter.bp, url_prefix='/webhooks/twitter/'
    )

    from .ses import ses_handler
    if not app.debug:
        app.logger.addHandler(ses_handler)

    return app


app = create_app()
