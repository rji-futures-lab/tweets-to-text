# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize boto3, the AWS Python API."""
import os
import boto3
from flask import g


def get_boto3session():
    """
    Get a boto3 session.

    Add to application content, g.boto3, if missing.

    Return a boto3 `Session` instance.
    """
    if 'boto3' not in g:
        config = dict(
            aws_access_key_id=os.getenv('BOTO3_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('BOTO3_SECRET_KEY'),
        )

        if os.getenv('BOTO3_REGION'):
            config['region_name'] = os.getenv('BOTO3_REGION')

        g.boto3 = boto3.Session(**config)

    return g.boto3
