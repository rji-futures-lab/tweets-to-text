"""
Unit tests.
"""

def test_index_view(client):
    """
    Confirm the homepage is up and running.
    """
    response = client.get('/')

    assert response.status_code == 200


def test_incoming_follow(client, requests_mock, incoming_follow):
    """
    Confirm that an incoming follow event results in a follow back.
    """
    requests_mock.register_uri(
        'POST', 
        'https://api.twitter.com/1.1/friendships/create.json',
        json=dict()
    )
    response = client.post(
        '/webhooks/twitter/',
        json=incoming_follow
    )

    assert response.get_json()['new_followers'] == 1


def test_outcoming_follow(client, requests_mock, outgoing_follow):
    """
    Confirm that an outgoing follow event does NOT cause a follow back.
    """
    requests_mock.register_uri(
        'POST',
        'https://api.twitter.com/1.1/friendships/create.json',
        json=dict()
    )
    response = client.post(
        '/webhooks/twitter/',
        json=outgoing_follow
    )

    assert response.get_json()['new_followers'] == 0
