"""Test behavior after follow events.."""
import pytest # noqa
from .context_setters import dynamodb_set
from tweets2text.handlers.twitter.follow import instructions

def test_incoming_follow_saved(
        app, mock_direct_messages_new, mock_typing_indicator,
        incoming_follow_activity, dynamodb
        ):
    """Confirm incoming follow event saved to account-activity table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=incoming_follow_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_outgoing_follow_saved(
        app, mock_direct_messages_new, mock_typing_indicator,
        outgoing_follow_activity, dynamodb
        ):
    """Confirm outgoing follow event saved to account-activity table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-account-activity'
            ).scan(Select='COUNT')['Count']
    assert table_scan == 1


def test_incoming_follow_dm_count(
        app, mock_direct_messages_new, mock_typing_indicator,
        incoming_follow_activity, dynamodb
        ):
    """Confirm only 1 Twitter API call after incoming follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=incoming_follow_activity
            )
    assert mock_direct_messages_new.call_count == len(instructions)


def test_outgoing_follow_dm_count(
        app, mock_direct_messages_new, mock_typing_indicator,
        outgoing_follow_activity, dynamodb
        ):
    """Confirm no Twitter API calls after outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_activity
            )
    assert mock_direct_messages_new.call_count == 0


def test_incoming_follow_response_count(
        app, mock_direct_messages_new, mock_typing_indicator,
        incoming_follow_activity, dynamodb
        ):
    """Confirm new_follower count of 1 after outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=incoming_follow_activity
            )
    assert response.get_json()['new_followers'] == 1


def test_outgoing_follow_response_count(
        app, mock_direct_messages_new, mock_typing_indicator,
        outgoing_follow_activity, dynamodb
        ):
    """Confirm new_follower count of 0 after outgoing follow event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=outgoing_follow_activity
            )
    assert response.get_json()['new_followers'] == 0
