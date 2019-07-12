import json
import random
from time import sleep
import uuid
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
from requests.exceptions import HTTPError
from TwitterAPI import TwitterPager
from .constants import instructions, replies
from tweets2text.twitter_api import (
    Tweet, TwitterMixin, TwitterObject, TwitterUser
)


class User(TwitterMixin, models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        editable=False,
    )
    id_str = models.CharField(
        max_length=200,
        editable=False,
    )
    name = models.CharField(
        max_length=200,
        editable=False,
    )
    screen_name = models.CharField(
        max_length=20,
        editable=False,
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        editable=False,
    )
    json_data = JSONField(
        editable=False,
        default=dict
    )
    last_follow_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    @property
    def has_pending_compilation(self):
        return self.compilations.pending().exists()

    @property
    def pending_compilation(self):
        return self.compilations.pending().latest('requested_at')

    def send_dm(self, message_text):
        """Send a direct message to follower containing message_text."""
        data = dict(
            event=dict(
                type="message_create",
                message_create=dict(
                    target=dict(recipient_id=self.id_str),
                    message_data=dict(text=message_text),
                )
            )
        )
        self.send_typing_indicator()
        if settings.THROTTLE_TWITTER_API_CALLS:
            sleep(3.1)

        sent_dm = self.twitter_api.request(
            'direct_messages/events/new',
            json.dumps(data),
        )

        return sent_dm

    def send_welcome_dm(self):
        for m in instructions:
            self.send_dm(m)

    def send_typing_indicator(self):
        params = dict(recipient_id=self.id_str)

        sent_indicator = self.twitter_api.request(
            'direct_messages/indicate_typing',
            params,
        )

        return sent_indicator

    def __str__(self):
        return '@%s' % self.screen_name

    class Meta:
        verbose_name = 'TweetsToText User'
        verbose_name_plural = 'TweetsToText Users'
        indexes = [
            models.Index(
                fields=['id_str', ],
                name='id_str_index',
            ),
            models.Index(
                fields=['last_follow_at', ],
                name='last_follow_at_index',
            ),
        ]


class FollowHistory(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='follow_history',
        editable=False,
    )
    event_json = JSONField(editable=False,)

    @property
    def type(self):
        return self.event_json['type']

    @property
    def created_timestamp(self):
        return int(self.event_json['created_timestamp'])

    @property
    def created_datetime(self):
        self._created_datetime = timezone.datetime.fromtimestamp(
            self.created_timestamp / 1000.0, tz=timezone.utc
        )
        return self._created_datetime

    def __str__(self):
        return '{0} on {1}'.format(
            self.event_json['type'], self.created_datetime
        )


class AccountActivity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    received_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    processing_started_at = models.DateTimeField(null=True, editable=False,)
    processing_completed_at = models.DateTimeField(null=True, editable=False,)
    json_data = JSONField(editable=False,)

    def get_events_by_type(self, message_type):
        try:
            event_list = [
                TwitterObject(**e) for e in self.json_data[message_type]
            ]
        except KeyError:
            event_list = []

        return event_list

    @property
    def direct_message_events(self):
        try:
            self._direct_message_events
        except AttributeError:
            self._direct_message_events = self.get_events_by_type(
                'direct_message_events'
            )

        return self._direct_message_events

    @property
    def follow_events(self):
        try:
            self._follow_events
        except AttributeError:
            bot_id = self.json_data['for_user_id']
            self._follow_events = [
                f for f in self.get_events_by_type('follow_events')
                if (
                    f.type == 'follow'
                    and TwitterUser(**f.target).id_str == bot_id
                    and TwitterUser(**f.source).id_str != bot_id
                )
            ]

        return self._follow_events

    @property
    def unfollow_events(self):
        try:
            self._unfollow_events
        except AttributeError:
            bot_id = self.json_data['for_user_id']
            self._unfollow_events = [
                f for f in self.get_events_by_type('unfollow_events')
                if (
                    f.type == 'unfollow'
                    and TwitterUser(**f.target).id_str == bot_id
                    and TwitterUser(**f.source).id_str != bot_id
                )
            ]

        return self._unfollow_events

    @property
    def tweet_create_events(self):
        try:
            self._tweet_create_events
        except AttributeError:
            try:
                self._tweet_create_events = [
                    Tweet(**e) for e in
                    self.json_data['tweet_create_events']
                ]
            except KeyError:
                self._tweet_create_events = []

        return self._tweet_create_events

    def __str__(self):
        return 'on {0}'.format(self.received_at)

    class Meta:
        verbose_name = 'Account Activity'
        verbose_name_plural = 'Account Activity'
        indexes = [
            models.Index(
                fields=['received_at', ],
                name='received_at_index',
            ),
        ]


class TweetTextCompilationManager(models.Manager):

    def completed(self):
        qs = self.get_queryset().filter(completed_at__isnull=False)

        return qs

    def pending(self):
        qs = self.get_queryset().filter(
            init_tweet_deleted=False, completed_at__isnull=True
        )

        return qs


class TweetTextCompilation(TwitterMixin, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='compilations',
        editable=False,
    )
    init_tweet_json = JSONField(editable=False,)
    final_tweet_json = JSONField(
        null=True,
        editable=False,
    )
    init_tweet_deleted = models.BooleanField(
        default=False,
        editable=False,
    )
    requested_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    completed_at = models.DateTimeField(
        null=True,
        editable=False,
    )
    tweets = ArrayField(
        JSONField(),
        default=list,
        editable=False,
    )
    text = models.TextField(
        blank=True,
        editable=False,
    )
    thread_only = models.BooleanField(
        default=False,
    )

    def complete(self):
        self.tweets = self.get_tweets()

        self.tweets.append(self.init_tweet_json)

        sorted_tweets = sorted(self.tweets, key=lambda k: k['id'])

        if self.thread_only:
            init_tweet = sorted_tweets.pop(0)
            threaded_tweets = [init_tweet]
            for tweet in sorted_tweets:
                if tweet['in_reply_to_status_id'] in [t['id'] for t in threaded_tweets]:
                    threaded_tweets.append(tweet)
                else:
                    break
            self.text = '\n\n'.join(
                [Tweet(**t).get_formatted_text() for t in threaded_tweets]
            )
        else:
            self.text = '\n\n'.join(
                [Tweet(**t).get_formatted_text() for t in sorted_tweets]
            )

        self.completed_at = timezone.now()

        return self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tweets2text:compilation', args=[str(self.id)])

    def get_tweets(self):

        params = dict(
            user_id=self.user.id_str,
            since_id=self.init_tweet.id_str,
            count=200,
            include_rts=True,
            tweet_mode='extended',
        )

        if self.final_tweet:
            params['max_id'] = self.final_tweet.id_str

        response = self.twitter_api.request(
            'statuses/user_timeline',
            params,
        )
        response.response.raise_for_status()

        if len(response.json()) > 199:
            pager = TwitterPager(
                self.twitter_api, 'statuses/user_timeline', params
            )
            tweets = []
            for i in pager.get_iterator(wait=3.5):
                tweets.append(i)
        else:
            tweets = response.json()

        return tweets

    def refresh_init_tweet(self):
        response = self.init_tweet.get_from_twitter()

        try:
            response.response.raise_for_status()
        except HTTPError:
            self.init_tweet_deleted = True
        else:
            self.init_tweet_json = response.json()

        return self.save()

    def reply_to_init_tweet(self):
        if settings.THROTTLE_TWITTER_API_CALLS:
            sleep(5)

        status = '@{0} {1}'.format(
            self.user.screen_name, random.choice(replies)
        )
        params = dict(
            status=status,
            in_reply_to_status_id=self.init_tweet.id_str,
        )

        return self.twitter_api.request('statuses/update', params)

    @property
    def init_tweet(self):
        return Tweet(**self.init_tweet_json)

    @property
    def final_tweet(self):
        try:
            tweet = Tweet(**self.final_tweet_json)
        except TypeError:
            tweet = None
        return tweet

    def __str__(self):
        return 'from {0} (on {1})'.format(
            self.user.screen_name, self.requested_at
        )

    objects = TweetTextCompilationManager()

    class Meta:
        indexes = [
            models.Index(
                fields=['requested_at', ],
                name='requested_at_index',
            ),
            models.Index(
                fields=['completed_at', ],
                name='completed_at_index',
            ),
        ]
