# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize AWS DynamoDB for data storage.
"""
import os
import click
from flask import current_app, g
from .boto3 import get_boto3session


def get_dynamodb():
    """
    Connect to DynamoDb.

    Add the connection to the Flask application context (`g.dynamodb`),
    if missing.

    Return a DynamoDB `Resource` instance.
    """
    if 'dynamodb' not in g:
        boto3session = get_boto3session()
        if os.getenv('FLASK_ENV') == 'development':
            endpoint_url = '{0}:{1}'.format(
                current_app.config['DYNAMO_LOCAL_HOST'],
                current_app.config['DYNAMO_LOCAL_PORT'],
            )
            g.dynamodb = boto3session.resource(
                'dynamodb', endpoint_url=endpoint_url
            )
        else:
            g.dynamodb = boto3session.resource('dynamodb')

    return g.dynamodb


def get_table(table_name):
    """
    Return a DynamoDB `Table` instance for table_name.
    """
    dynamodb = get_dynamodb()

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
        TableName='account-activity',
        KeySchema=[
            dict(AttributeName='created_at', KeyType='HASH'),
        ],
        AttributeDefinitions=[
            dict(AttributeName='created_at', AttributeType='S'),
        ],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
    ),
    dict(
        TableName='jobs',
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
        TableName='webhooks',
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
