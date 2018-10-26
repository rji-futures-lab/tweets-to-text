# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Custom commands for managing tweet2text's integration with AWS S3."""
import os
from urllib.parse import urljoin
import click
from flask.cli import AppGroup, with_appcontext
from boto3.dynamodb.conditions import Key, Attr
from tweets2text.dynamodb import get_table
from tweets2text.twitter_api import get_api


twitter_cli = AppGroup('twitter')


def get_latest_webhook_id(webhooks_table):
    """Return id of the most recent valid webhook."""
    q = webhooks_table.query(
        KeyConditionExpression=Key('env_name').eq(
            os.getenv('TWITTER_API_ENV')
        ),
        FilterExpression=Attr('valid').eq(True),
        ScanIndexForward=False,
    )
    if len(q['Items']) > 0:
        webhook_id = q['Items'][0]['id']
    else:
        webhook_id = None
    return webhook_id


@twitter_cli.command('delete-webhook')
@click.option('--webhook_id', '-id', type=int)
@with_appcontext
def delete_current_webhook_command(webhook_id):
    """
    Delete a webhook registered with Twitter.

    Unless id provided, delete the most recent valid webhook.

    Set valid to `False` in webhooks DynamoDB table.
    """
    webhooks_table = get_table('webhooks')

    if not webhook_id:
        webhook_id = get_latest_webhook_id(webhooks_table)

    if not webhook_id:
        click.echo('No webhooks currently registered.')
    else:
        response = get_api().request(
            'account_activity/all/:{env}/webhooks/:{id}'.format(
                env=os.getenv('TWITTER_API_ENV'),
                id=webhook_id
            ),
            method_override='DELETE'
        )
        response.response.raise_for_status()
        webhooks_table.update_item(
            Key={
                'env_name': os.getenv('TWITTER_API_ENV'),
                'id': webhook_id
            },
            UpdateExpression='SET valid = :val1',
            ExpressionAttributeValues={':val1': False},
        )
        click.echo('webhook_id %s deleted.' % webhook_id)


@twitter_cli.command('get-subscription-info')
@with_appcontext
def get_subscription_info_command():
    """Get Twitter account activity subscription info."""
    # TODO: does this command even work?
    response = get_api().request(
        'account_activity/all/count',
    )
    response.response.raise_for_status()
    click.echo(response.status_code)
    click.echo(response.response.reason)


@twitter_cli.command('get-webhook-info')
@with_appcontext
def get_webhook_info_command():
    """
    Get webhooks currently registered with Twitter.

    Put each item in the webhooks DynamoDB table.
    """
    response = get_api().request(
        'account_activity/all/webhooks'
    )
    response.response.raise_for_status()

    data = response.response.json()
    for env in data['environments']:
        click.echo(env['environment_name'])
        for wh in env['webhooks']:
            click.echo(wh)
            wh['env_name'] = env['environment_name']
            get_table('webhooks').put_item(Item=wh)


@twitter_cli.command('register-webhook')
@click.argument('domain', type=click.STRING)
@with_appcontext
def register_webhook_command(domain):
    """
    Register a webhook under domain with Twitter.

    Put each item in the webhooks DynamoDB table.
    """
    url = urljoin(domain, 'webhooks/twitter/')
    response = get_api().request(
        'account_activity/all/:{}/webhooks'.format(
            os.getenv('TWITTER_API_ENV'),
        ),
        params={'url': url},
    )
    response.response.raise_for_status()
    item = response.response.json()
    item['env_name'] = os.getenv('TWITTER_API_ENV')
    get_table('webhooks').put_item(Item=item)
    click.echo(item)


@twitter_cli.command('subscribe-to-user')
@with_appcontext
def subscribe_to_user_command():
    """Subscribe to account activity for the user."""
    response = get_api().request(
        'account_activity/all/:{}/subscriptions'.format(
            os.getenv('TWITTER_API_ENV'),
        ),
        method_override='POST'
    )
    response.response.raise_for_status()
    click.echo(response.status_code)
    click.echo(response.response.reason)


@twitter_cli.command('validate-webhook')
@click.option('--id', type=int)
@with_appcontext
def validate_webhook_command(webhook_id):
    """
    Validate a webhook with Twitter.

    Unless id provided, validate the most recent valid webhook.
    """
    webhooks_table = get_table('webhooks')

    if not webhook_id:
        webhook_id = get_latest_webhook_id(webhooks_table)

    if not webhook_id:
        click.echo('No webhooks currently registered.')

    response = get_api().request(
        'account_activity/all/:{env}/webhooks/:{id}'.format(
            env=os.getenv('TWITTER_API_ENV'),
            id=webhook_id,
        ),
        method_override='PUT'
    )
    response.response.raise_for_status()
    # TODO: store the last_validated_at value?
    click.echo(response.status_code)
    click.echo(response.response.reason)
