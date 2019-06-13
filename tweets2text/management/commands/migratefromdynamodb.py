"""Migrate data from DynamoDB into PostgreSQL."""
import configparser
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from tweets2text.models import (
    AccountActivity, TweetTextCompilation, User
)
from tweets2text.twitter_api import TwitterUser
import boto3
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Migrate data from DynamoDB into PostgreSQL."""

    help = "Migrate data from DynamoDB into PostgreSQL."

    def add_arguments(self, parser):
        parser.add_argument('start_key', type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        """Handle the command."""
        if self.table.item_count != AccountActivity.objects.count():
            self.scanned_count = 0

            if options['start_key']:
                scan = self.table.scan(
                    ExclusiveStartKey=dict(created_at=options['start_key'])
                    )
                self.scanned_count = AccountActivity.objects.count()
            else:
                scan = self.table.scan()
                self.scanned_count = 0

            self.stdout.write(
                '  Total items to scan: %s' % self.table.item_count
            )

            scan = self.table.scan()

            self.handle_scan(scan)

            while 'LastEvaluatedKey' in scan.keys():
                scan = self.table.scan(
                    ExclusiveStartKey=scan['LastEvaluatedKey']
                )
                self.handle_scan(scan)
                if 'LastEvaluatedKey' in scan.keys():
                    self.stdout.write(
                        '  LastEvaluatedKey: %s' % scan['LastEvaluatedKey']
                    )

            assert self.table.item_count == self.scanned_count
            assert self.table.item_count == AccountActivity.objects.count()

        for activity in AccountActivity.objects.order_by('received_at'):
            self.process_account_activity(activity)

    @property
    def boto3_session(self):
        self._boto3_session = boto3.Session(**self.boto3_credentials)

        return self._boto3_session

    @property
    def boto3_credentials(self):
        secrets = configparser.RawConfigParser()
        secrets.read(os.path.join(settings.ROOT_DIR, 'secrets.cfg'))
        secrets = secrets['prod']
        self._boto3_credentials = dict(
            aws_access_key_id=secrets.get('aws_access_key_id'),
            aws_secret_access_key=secrets.get('aws_secret_access_key'),
            region_name='us-east-1',
        )
        return self._boto3_credentials

    @property
    def dynamodb(self):
        self._dynamodb = self.boto3_session.resource('dynamodb')
        return self._dynamodb

    @property
    def table(self):
        self._table = self.dynamodb.Table('TweetsToText-account-activity')
        return self._table

    def process_account_activity(self, account_activity):
        account_activity.processing_started_at = timezone.now()

        for follow in account_activity.follow_events:
            try:
                user = User.objects.get(id=follow.source['id'])
            except User.DoesNotExist:
                user = User.objects.create(
                    id=follow.source['id'],
                    id_str=TwitterUser(**follow.source).id_str,
                    name=follow.source['name'],
                    screen_name=follow.source['screen_name'],
                    location=follow.source['location'],
                    json_data=follow.source,
                    last_follow_at=self.timestamp_to_tz_aware(
                        follow.created_timestamp
                    ),
                )
            else:
                user.last_follow_at = self.timestamp_to_tz_aware(follow.created_timestamp)
                user.save()

            user.follow_history.create(event_json=follow.__dict__)

        for unfollow in account_activity.unfollow_events:
            user = User.objects.get(id=unfollow.source['id'])
            user.follow_history.create(event_json=unfollow.__dict__)

        for tweet in account_activity.tweet_create_events:
            try:
                user = tweet.user_obj.as_tweets2text_user
            except User.DoesNotExist:
                user = User.objects.create(
                    id=tweet.user_obj.id,
                    id_str=tweet.user_obj.id_str,
                    name=tweet.user_obj.name,
                    screen_name=tweet.user_obj.screen_name,
                    location=tweet.user_obj.location or '',
                    json_data=tweet.user,
                )

            if user.has_pending_compilation:
                user.pending_compilation.refresh_init_tweet()

            if user.has_pending_compilation:
                pending_compilation = user.pending_compilation
                pending_compilation.final_tweet_json = tweet.__dict__
                pending_compilation.save()
                pending_compilation.complete()
            else:
                created_at_dt = timezone.datetime.strptime(
                    tweet.created_at, "%a %b %d %H:%M:%S %z %Y"
                ).replace(tzinfo=timezone.utc)

                TweetTextCompilation.objects.create(
                    user=user,
                    init_tweet_json=tweet.__dict__,
                    requested_at=created_at_dt,
                )

        account_activity.processing_completed_at = timezone.now()

        return account_activity.save()

    def handle_scan(self, scan):
        self.scanned_count += scan['ScannedCount']

        objs = [
            AccountActivity(
                received_at=self.isoformat_to_tz_aware(item['created_at']),
                json_data=json.loads(item['account_activity']),
            ) for item in scan['Items']
        ]

        AccountActivity.objects.bulk_create(objs)

        self.stdout.write(
            '  Items currently scanned: %s' % self.scanned_count
        )

    def isoformat_to_tz_aware(self, dt_str):
        dt = timezone.datetime.strptime(
            dt_str, "%Y-%m-%dT%H:%M:%S.%f"
        ).replace(tzinfo=timezone.utc)
        return dt

    def timestamp_to_tz_aware(self, timestamp):
        dt = timezone.datetime.fromtimestamp(int(timestamp)/1000.0, tz=timezone.utc)
        return dt
