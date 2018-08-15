# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize AWS S3 for text file buckets.
"""
import os
from urllib.parse import urlunparse
from flask import current_app, g
from .boto3 import get_boto3session


def get_s3():
    """
    Connect to S3.

    Add the connection to the Flask application context (`g.s3`),
    if missing.

    Return an S3 `Resource` instance.
    """
    if 's3' not in g:
        boto3session = get_boto3session()
        g.s3 = boto3session.resource('s3')

    return g.s3


def get_bucket():
    """
    Returns a boto3 `Bucket` instance for `S3_BUCKET_NAME` (defined in config).
    """
    s3 = get_s3()

    return s3.Bucket(current_app.config['S3_BUCKET_NAME'])


def get_s3_file_url(key):
    """
    Returns a url to key in the app's S3 bucket.
    """
    netloc = 's3.%s.amazonaws.com' % current_app.config['REGION']
    path = '{0}/{1}'.format(current_app.config['S3_BUCKET_NAME'], key)
    return urlunparse(('https', netloc, path, '', '', ''))
