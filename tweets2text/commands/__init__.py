# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom commands for managing an instance of the tweets2text app.
"""
from .dynamodb import dynamodb_cli 
# from .s3 import s3_cli
from .twitter import twitter_cli


# TODO (maybe): Make these "custom scripts" that aren't loaded by FLASK_APP
# http://flask.pocoo.org/docs/1.0/cli/?highlight=commands#custom-scripts
def add_all(app):
    """
    Add all custom commands to an app instance.
    """
    # app.cli.add_command(dynamodb.create_all_tables_command)
    app.cli.add_command(dynamodb_cli)
    # app.cli.add_command(s3_cli)
    app.cli.add_command(twitter_cli)

