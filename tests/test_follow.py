"""Test behavior after follow events.."""
import pytest # noqa
from .context_setters import dynamodb_set


def test_incoming_follow_saved(
        app, mock_direct_messages_new, incoming_follow_data, dynamodb
        ):
    """Confirm incoming follow event saved to account-activity table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_outgoing_follow_saved(
        app, mock_direct_messages_new, outgoing_follow_data, dynamodb
        ):
    """Confirm outgoing follow event saved to account-activity table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_incoming_follow_dm_count(
        app, mock_direct_messages_new, incoming_follow_data, dynamodb
        ):
    """Confirm only 1 Twitter API call in response to incoming follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
    assert mock_direct_messages_new.call_count == 1


def test_outgoing_follow_dm_count(
        app, mock_direct_messages_new, outgoing_follow_data, dynamodb
        ):
    """Confirm no Twitter API calls in response to outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
    assert mock_direct_messages_new.call_count == 0


def test_incoming_follow_response_count(
        app, mock_direct_messages_new, incoming_follow_data, dynamodb
        ):
    """Confirm new_follower count of 1 in response to outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=incoming_follow_data
            )
    assert response.get_json()['new_followers'] == 1


def test_outgoing_follow_response_count(
        app, mock_direct_messages_new, outgoing_follow_data, dynamodb
        ):
    """Confirm new_follower count of 0 in response to outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_data
            )
    assert response.get_json()['new_followers'] == 0
