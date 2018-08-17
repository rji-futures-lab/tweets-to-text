# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize AWS DynamoDB for data storage.
"""
import os
from .boto3 import get_boto3session


def get_dynamodb():
    """
    Connect to DynamoDB.

    Return a DynamoDB `Resource` instance.
    """
    boto3session = get_boto3session()

    is_local_host = bool(
        os.getenv('DYNAMO_LOCAL_HOST') and os.getenv('DYNAMO_LOCAL_PORT')
    )

    if is_local_host:
        endpoint_url = '{0}:{1}'.format(
            os.getenv('DYNAMO_LOCAL_HOST'),
            os.getenv('DYNAMO_LOCAL_PORT'),
        )
        dynamodb = boto3session.resource(
            'dynamodb', endpoint_url=endpoint_url
        )
    else:
        dynamodb = boto3session.resource('dynamodb')

    return dynamodb


def get_table(table_name):
    """
    Return a DynamoDB `Table` instance for table_name.
    """
    dynamodb = get_dynamodb()
    if not table_name.startswith('TweetsToText'):
        table_name = 'TweetsToText-' + table_name

    return dynamodb.Table(table_name)


def get_table_schema(table_name):
    """
    Return a dict with the schema definition of table_name.

    If no schema is defined for table_name, return None.
    """
    try:
        table_schema = [i for i in schema if i['TableName'] == table_name][0]
    except IndexError:
        table_schema = None
    return table_schema


schema = [
    dict(
        TableName='TweetsToText-account-activity',
        KeySchema=[
            dict(AttributeName='created_at', KeyType='HASH'),
        ],
        AttributeDefinitions=[
            dict(AttributeName='created_at', AttributeType='S'),
        ],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
    ),
    dict(
        TableName='TweetsToText-jobs',
        KeySchema=[
            dict(AttributeName='user_id', KeyType='HASH'),
            dict(AttributeName='init_tweet_id', KeyType='RANGE')
        ],
        AttributeDefinitions=[
            dict(AttributeName='user_id', AttributeType='N'),
            dict(AttributeName='init_tweet_id', AttributeType='N'),
        ],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
    ),
    dict(
        TableName='TweetsToText-webhooks',
        KeySchema=[
            dict(AttributeName='env_name', KeyType='HASH'),
            dict(AttributeName='id', KeyType='RANGE'),
        ],
        AttributeDefinitions=[
            dict(AttributeName='env_name', AttributeType='S'),
            dict(AttributeName='id', AttributeType='S'),
        ],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
    ),
]
