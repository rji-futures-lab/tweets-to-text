import re
from django.test import Client
from requests_mock import Mocker
from tweets2text.models import AccountActivity
from tweets2text import fixtures


class AccountActivityTestBase:
    """Base test case for account activity events."""

    account_activity = None

    def setUp(self):

        self.client = Client()

        self.webhook_response = self.client.post(
            '/webhooks/twitter/',
            data=self.account_activity,
            content_type="application/json",
        )

    def test_account_activity_count(self):
        aa_count = AccountActivity.objects.count()
        self.assertEqual(aa_count, 1)

    def test_webhook_response_success(self):
        self.assertEqual(self.webhook_response.status_code, 200)

    def test_account_activity_processing_completed_at(self):
        aa = AccountActivity.objects.all()[0]
        self.assertTrue(aa.processing_completed_at)


class FollowTestBase(AccountActivityTestBase):
    """Base test case for follow events."""

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

        super(FollowTestBase, self).setUp()


class CreateTweetBaseTest(AccountActivityTestBase):
    """Base test case for create tweet events."""

    friendship_lookup_response = [dict(connections=['followed_by'])]

    @Mocker()
    def setUp(self, m):

        friendship_lookup_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/friendships/lookup\.json\?user_id\=\d+' # noqa
        )
        self.mock_friendship_lookup_endpoint = m.register_uri(
            'GET',
            friendship_lookup_url_pattern,
            json=self.friendship_lookup_response,
        )

        self.mock_dm_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/events/new.json',
            json=dict()
        )

        statuses_show_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/statuses/show\/\d+\.json'
        )
        self.mock_statuses_show_endpoint = m.register_uri(
            'GET',
            statuses_show_url_pattern,
            json=fixtures.init_mention_w_full_text,
        )

        self.mock_statuses_update_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/statuses/update.json',
            json=dict()
        )

        self.mock_typing_indicator_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/indicate_typing.json',
            json=dict()
        )

        self.mock_user_timeline_endpoint = m.register_uri(
            'GET',
            'https://api.twitter.com/1.1/statuses/user_timeline.json',
            json=fixtures.tweets
        )

        super(CreateTweetBaseTest, self).setUp()


class ThreadedTweetBaseTest(AccountActivityTestBase):
    """Base test case for threaded tweets."""

    account_activity = fixtures.account_activity_w_threaded_final_mention
    friendship_lookup_response = [dict(connections=['followed_by'])]

    @Mocker()
    def setUp(self, m):

        friendship_lookup_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/friendships/lookup\.json\?user_id\=\d+' # noqa
        )
        self.mock_friendship_lookup_endpoint = m.register_uri(
            'GET',
            friendship_lookup_url_pattern,
            json=self.friendship_lookup_response,
        )

        self.mock_dm_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/events/new.json',
            json=dict()
        )

        statuses_show_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/statuses/show\/\d+\.json'
        )
        self.mock_statuses_show_endpoint = m.register_uri(
            'GET',
            statuses_show_url_pattern,
            json=fixtures.init_mention_w_full_text,
        )

        self.mock_statuses_update_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/statuses/update.json',
            json=dict()
        )

        self.mock_typing_indicator_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/indicate_typing.json',
            json=dict()
        )

        self.mock_user_timeline_endpoint = m.register_uri(
            'GET',
            'https://api.twitter.com/1.1/statuses/user_timeline.json',
            json=fixtures.threaded_tweets
        )

        super(ThreadedTweetBaseTest, self).setUp()
