from django.test import TestCase
from django.utils import timezone
from tweets2text.constants import instructions
from tweets2text import fixtures
from tweets2text.models import User
from .base import FollowTestBase


class FollowTestCase(FollowTestBase, TestCase):
    """Test case for receiving a follow event."""

    account_activity = fixtures.account_activity_w_follow_event

    def test_user_count(self):
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_dm_call_count(self):
        self.assertEqual(
            len(instructions),
            self.mock_dm_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            len(instructions),
            self.mock_typing_indicator_endpoint.call_count
        )

    def test_follow_history_count(self):
        user = User.objects.get(
            id_str=fixtures.user['id_str']
        )
        count = user.follow_history.filter(
            event_json__type='follow'
        ).count()

        self.assertEqual(1, count)


class UnfollowTestCase(FollowTestBase, TestCase):
    """Test case for receiving an unfollow event."""

    account_activity = fixtures.account_activity_w_unfollow_event

    @classmethod
    def setUpTestData(cls):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        User.objects.create(**user_data)

    def test_user_count(self):
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_typing_indicator_endpoint.call_count
        )

    def test_follow_history_count(self):
        user = User.objects.get(
            id_str=fixtures.user['id_str']
        )
        count = user.follow_history.filter(
            event_json__type='unfollow'
        ).count()

        self.assertEqual(1, count)


class RefollowTestCase(FollowTestBase, TestCase):
    """Test case for receiving returning follower event."""

    account_activity = fixtures.account_activity_w_follow_event

    @classmethod
    def setUpTestData(cls):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        user_data['last_follow_at'] = timezone.datetime(
            1980, 11, 13, tzinfo=timezone.utc
        )
        user = User.objects.create(**user_data)
        user.follow_history.create(event_json=fixtures.follow_event)

    def test_dm_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            1, self.mock_typing_indicator_endpoint.call_count
        )

    def test_follow_history_count(self):
        user = User.objects.all()[0]
        count = user.follow_history.filter(
            event_json__type='follow'
        ).count()

        self.assertEqual(2, count)

    def test_last_follow_at(self):
        user = User.objects.all()[0]
        self.assertEqual(
            timezone.now().year,
            user.last_follow_at.year,
        )


class BotFollowSourceTestCase(FollowTestBase, TestCase):
    """Test case for receiving follow event by the bot."""

    account_activity = fixtures.account_activity_w_bot_event

    def test_user_not_created(self):
        count = User.objects.count()
        self.assertEqual(0, count)

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_typing_indicator_endpoint.call_count
        )
