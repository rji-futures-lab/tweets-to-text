# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize AWS S3 for text file buckets.
"""
import os
from urllib.parse import urlunparse
from flask import g
from .boto3 import get_boto3session


def get_s3():
    """
    Get a connection to to AWS S3.

    Add to g.s3, if missing.

    Return an S3 `Resource` instance.
    """
    if 's3' not in g:
        boto3session = get_boto3session()
        g.s3 = boto3session.resource('s3')

    return g.s3


def get_bucket():
    """
    Get the bucket for `S3_BUCKET_NAME` (defined in config).
    
    Add to g.s3_bucket, if missing.

    Returns a boto3 `Bucket` instance.
    """
    if 's3_bucket' not in g:
        s3 = get_s3()
        g.s3_bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))

    return g.s3_bucket


def get_s3_file_url(key):
    """
    Returns a url to key in the app's S3 bucket.
    """

    netloc = 's3.%s.amazonaws.com' % os.getenv('BOTO3_REGION')
    path = '{0}/{1}'.format(os.getenv('S3_BUCKET_NAME'), key)

    return urlunparse(('https', netloc, path, '', '', ''))
