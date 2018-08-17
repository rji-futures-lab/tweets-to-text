# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize boto3, the AWS Python API.
"""
import os
import boto3


def get_boto3session():
    """
    Initialize a boto3 session. Return a Session instance.
    """
    config = dict(
        aws_access_key_id=os.getenv('BOTO3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('BOTO3_SECRET_KEY'),        
    )

    if os.getenv('BOTO3_REGION'):
        config['region_name'] = os.getenv('BOTO3_REGION')

    return boto3.Session(**config)
