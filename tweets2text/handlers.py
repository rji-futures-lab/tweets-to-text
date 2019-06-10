from django.utils import timezone
from zappa.async import task
from tweets2text.models import (
    AccountActivity, TweetTextCompilation, User
)


@task(capture_response=True)
def handle_account_activity(account_activity_id):

    activity = AccountActivity.objects.get(id=account_activity_id)
    activity.processing_started_at = timezone.now()

    for follow in activity.follow_events:
        try:
            user = User.objects.get(id=follow.source['id'])
        except User.DoesNotExist:
            user = User.objects.create(
                id=follow.source['id'],
                id_str=follow.source['id_str'],
                name=follow.source['name'],
                screen_name=follow.source['screen_name'],
                location=follow.source['location'],
                json_data=follow.source,
            )
            user.send_welcome_dm()
        else:
            user.last_follow_at = timezone.now()
            user.save()
            user.send_dm('Welcome back!')

        user.follow_history.create(event_json=follow.__dict__)

    for unfollow in activity.unfollow_events:
        user = User.objects.get(id=unfollow.source['id'])
        user.follow_history.create(event_json=unfollow.__dict__)

    for tweet in activity.tweet_create_events:
        if tweet.is_actionable_mention:
            user = tweet.user_obj.as_tweets2text_user

            if user.has_pending_compilation:
                user.pending_compilation.refresh_init_tweet()

            if user.has_pending_compilation:
                pending_compilation = user.pending_compilation
                pending_compilation.final_tweet_json = tweet.__dict__
                pending_compilation.save()
                pending_compilation.complete()
                url = pending_compilation.get_absolute_url()
                user.send_dm(url)

            else:
                new_compilation = TweetTextCompilation.objects.create(
                    user=user, init_tweet_json=tweet.__dict__
                )
                new_compilation.reply_to_init_tweet()

    activity.processing_completed_at = timezone.now()

    return activity.save()
