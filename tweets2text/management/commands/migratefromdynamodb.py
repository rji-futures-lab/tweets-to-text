"""Migrate data from DynamoDB into PostgreSQL."""
import configparser
import json
import os
import uuid
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from tweets2text.models import (
    AccountActivity, TweetTextCompilation, User
)
from tweets2text.twitter_api import Tweet, TwitterUser
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
        self.stdout.write('=====dealing with account-activity=====')
        if self.account_activity_table.item_count != AccountActivity.objects.count():
            self.account_activity_scanned_count = 0

            if options['start_key']:
                scan = self.account_activity_table.scan(
                    ExclusiveStartKey=dict(created_at=options['start_key'])
                    )
                self.account_activity_scanned_count = AccountActivity.objects.count()
            else:
                scan = self.account_activity_table.scan()
                self.account_activity_scanned_count = 0


            self.stdout.write(
                '  Total items to scan: %s' % self.account_activity_table.item_count
            )

            scan = self.account_activity_table.scan()

            self.handle_account_activity_scan(scan)

            while 'LastEvaluatedKey' in scan.keys():
                scan = self.account_activity_table.scan(
                    ExclusiveStartKey=scan['LastEvaluatedKey']
                )
                self.handle_account_activity_scan(scan)
                if 'LastEvaluatedKey' in scan.keys():
                    self.stdout.write(
                        '  LastEvaluatedKey: %s' % scan['LastEvaluatedKey']
                    )

            assert self.account_activity_table.item_count == self.account_activity_scanned_count
            assert self.account_activity_table.item_count == AccountActivity.objects.count()

        for activity in AccountActivity.objects.order_by('received_at'):
            self.process_account_activity(activity)

        self.stdout.write('========dealing with jobs========')

        scan = self.jobs_table.scan()
        self.jobs_scanned_count = 0

        self.handle_jobs_scan(scan)

        while 'LastEvaluatedKey' in scan.keys():
            scan = self.jobs.scan(
                ExclusiveStartKey=scan['LastEvaluatedKey']
            )
            self.handle_jobs_scan(scan)
            if 'LastEvaluatedKey' in scan.keys():
                self.stdout.write(
                    '  LastEvaluatedKey: %s' % scan['LastEvaluatedKey']
                )

        assert self.jobs_table.item_count == self.jobs_scanned_count
        assert self.jobs_table.item_count == TweetTextCompilation.objects.count()

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
    def s3(self):
        self._s3 = self.boto3_session.resource('s3')
        return self._s3

    @property
    def downloads_bucket(self):
        self._downloads_bucket = self.s3.Bucket('tweets-to-text-downloads')
        return self._downloads_bucket

    @property
    def account_activity_table(self):
        self._account_activity_table = self.dynamodb.Table('TweetsToText-account-activity')
        return self._account_activity_table

    @property
    def jobs_table(self):
        self._jobs_table = self.dynamodb.Table('TweetsToText-jobs')
        return self._jobs_table

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

        account_activity.processing_completed_at = timezone.now()

        return account_activity.save()

    def handle_account_activity_scan(self, scan):
        self.account_activity_scanned_count += scan['ScannedCount']
        assert self.account_activity_scanned_count <= self.account_activity_table.item_count

        objs = [
            AccountActivity(
                received_at=self.isoformat_to_tz_aware(item['created_at']),
                json_data=json.loads(item['account_activity']),
            ) for item in scan['Items']
        ]

        AccountActivity.objects.bulk_create(objs)

        self.stdout.write(
            '  Items currently scanned: %s' % self.account_activity_scanned_count
        )

    def handle_jobs_scan(self, scan):
        self.jobs_scanned_count += scan['ScannedCount']

        for item in scan['Items']:
            
            init_tweet = Tweet(**json.loads(item['init_event_json']))

            try:
                user = User.objects.get(id=init_tweet.user_obj.id)
            except User.DoesNotExist:
                user = User.objects.create(
                    id=init_tweet.user_obj.id,
                    id_str=init_tweet.user_obj.id_str,
                    name=init_tweet.user_obj.name,
                    screen_name=init_tweet.user_obj.screen_name,
                    location=init_tweet.user_obj.location or '',
                    json_data=init_tweet.user,
                )

            data = dict(
                user=user,
                init_tweet_json=init_tweet.__dict__,
                requested_at=self.utc_str_to_tz_aware(init_tweet.created_at),
            )

            if 's3_key' in item.keys():
                data['id'] = item['s3_key'].strip('.txt')
                data['text'] = self.read_from_s3(item['s3_key'])
            else:
                data['id'] = str(uuid.uuid4())

            if 'final_event_json' in item.keys():
                final_tweet = Tweet(**json.loads(item['final_event_json']))
                data['final_tweet_json'] = final_tweet.__dict__
                data['completed_at'] = self.utc_str_to_tz_aware(
                    final_tweet.created_at
                )

            if 'tweets' in item.keys():
                data['tweets'] = json.loads(item['tweets'])


            TweetTextCompilation.objects.create(**data)

        self.stdout.write(
            '  Items currently scanned: %s' % self.jobs_scanned_count
        )

    def isoformat_to_tz_aware(self, dt_str):
        dt = timezone.datetime.strptime(
            dt_str, "%Y-%m-%dT%H:%M:%S.%f"
        ).replace(tzinfo=timezone.utc)
        return dt

    def timestamp_to_tz_aware(self, timestamp):
        dt = timezone.datetime.fromtimestamp(int(timestamp)/1000.0, tz=timezone.utc)
        return dt

    def utc_str_to_tz_aware(self, utc_str):
        dt = timezone.datetime.strptime(
            utc_str, "%a %b %d %H:%M:%S %z %Y"
        ).replace(tzinfo=timezone.utc)
        return dt

    def read_from_s3(self, key):
        obj = self.downloads_bucket.Object(key)

        return obj.get()['Body'].read().decode('utf-8')
