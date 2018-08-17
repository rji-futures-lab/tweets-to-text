# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize AWS S3 for text file buckets.
"""
import os
from urllib.parse import urlunparse
from dotenv import load_dotenv
from .boto3 import get_boto3session


def get_s3():
    """
    Connect to S3.

    Return an S3 `Resource` instance.
    """
    boto3session = get_boto3session()
    s3 = boto3session.resource('s3')

    return s3


def get_bucket():
    """
    Returns a boto3 `Bucket` instance for `S3_BUCKET_NAME` (defined in config).
    """
    s3 = get_s3()

    if not os.getenv('S3_BUCKET_NAME'):
        load_dotenv()

    return s3.Bucket(os.getenv('S3_BUCKET_NAME'))


def get_s3_file_url(key):
    """
    Returns a url to key in the app's S3 bucket.
    """
    if not os.getenv('BOTO3_REGION'):
        load_dotenv()

    netloc = 's3.%s.amazonaws.com' % os.getenv('BOTO3_REGION')
    path = '{0}/{1}'.format(os.getenv('S3_BUCKET_NAME'), key)

    return urlunparse(('https', netloc, path, '', '', ''))
