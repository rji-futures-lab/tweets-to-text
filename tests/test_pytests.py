from contextlib import contextmanager
from flask import appcontext_pushed, g
import pytest
from tweets2text.dynamodb import get_dynamodb


@contextmanager
def dynamodb_set(app, dynamodb_client):
    """
    Add local dynamodb fixture to the global app context.
    """
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_client
    with appcontext_pushed.connected_to(handler, app):
        yield


def test_incoming_follow_saved(
        app, mock_friendships_create, incoming_follow_data, dynamodb
    ):
    """
    Confirm incoming follow event is saved to account-activity DynamoDb table.
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_outgoing_follow_saved(
        app, mock_friendships_create, outgoing_follow_data, dynamodb
    ):
    """
    Confirm outgoing follow event is saved to account-activity DynamoDb table.
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_incoming_follow_call_count(
        app, mock_friendships_create, incoming_follow_data, dynamodb       
    ):
    """
    Confirm only 1 Twitter API call in response to incoming follow event
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
    assert mock_friendships_create.call_count == 1


def test_outgoing_follow_call_count(
        app, mock_friendships_create, outgoing_follow_data, dynamodb
    ):
    """
    Confirm no Twitter API calls in response to a an outgoing follow event.
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
    assert mock_friendships_create.call_count == 0


def test_incoming_follow_response_count(
        app, mock_friendships_create, incoming_follow_data, dynamodb
    ):
    """
    Confirm new_follower count of 1 in response to an outgoing follow event.
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
    assert response.get_json()['new_followers'] == 1


def test_outgoing_follow_response_count(
        app, mock_friendships_create, outgoing_follow_data, dynamodb
    ):
    """
    Confirm new_follower count of 0 in response to an outgoing follow event.
    """
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
    assert response.get_json()['new_followers'] == 0


def test_init_mention_new_job(
        app, dynamodb, init_mention, mock_statuses_update
    ):
    """Confirm that an initial mention creates a new job."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=init_mention
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_init_mention_call_count(
        app, dynamodb, init_mention, mock_statuses_update
    ):
    """Confirm that an initial mention creates a new job."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=init_mention
            )
    assert mock_statuses_update.call_count == 1
