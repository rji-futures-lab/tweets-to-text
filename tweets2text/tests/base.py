from django.test import Client, TestCase
from requests_mock import Mocker
from tweets2text.models import AccountActivity


class FollowBaseTestCase(TestCase):
    """Base test case for follow events."""
    account_activity = None

    @Mocker()
    def setUp(self, m):

        self.mock_dm_endpoint = m.register_uri(
            'POST', 
            'https://api.twitter.com/1.1/direct_messages/events/new.json',
            json=dict()
        )
        self.mock_typing_indicator_endpoint = m.register_uri(
            'POST', 
            'https://api.twitter.com/1.1/direct_messages/indicate_typing.json',
            json=dict()
        )

        self.client = Client()

        self.response = self.client.post(
            '/webhooks/twitter/',
            data=self.account_activity,
            content_type="application/json",
        )

    def test_account_activity_count(self):
        aa_count = AccountActivity.objects.count()
        self.assertEqual(aa_count, 1)

    def test_response_success(self):
        self.assertEqual(self.response.status_code, 200)
