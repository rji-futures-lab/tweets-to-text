# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize boto3, the AWS Python API.
"""
from flask import current_app, g
import boto3


def get_boto3session():
    """
    Initialize a boto3 session.

    Add the boto3 session to the Flask application context (`g.boto3session`),
    if missing.

    Return a Session instance.
    """
    if 'boto3session' not in g:
        g.boto3session = boto3.Session(
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['REGION'],
        )

    return g.boto3session
