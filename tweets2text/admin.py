import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin
from django.db.models import (
    Case, CharField, Count, Func, IntegerField, Q, Value, When
)
from django.contrib.postgres.fields import JSONField
from django.utils.safestring import mark_safe
from .models import (
    AccountActivity, TweetTextCompilation, User
)


class JSONArrayLength(Func):
    """
    Returns the length of a JSON array.
    """
    function = 'JSONB_ARRAY_LENGTH'
    output_field = IntegerField()


class JSONExtractPath(Func):
    """
    Returns JSON value pointed to by key.
    """
    template = "JSONB_EXTRACT_PATH(%(expressions)s, '%(key)s')"
    output_field = JSONField()

    def __init__(self, expression, key):
        """
        Create an instance.
        """
        super(JSONExtractPath, self).__init__(expression, key=key)


@admin.register(AccountActivity)
class AccountActivityAdmin(admin.ModelAdmin):
    date_hierarchy = 'received_at'
    list_display = (
        'id', 'received_at', 'processing_started_at', 'processing_completed_at',
        'follow_event_count', 'unfollow_event_count', 'tweet_create_event_count'
    )
    readonly_fields = (
        'id', 'received_at', 'processing_started_at', 'processing_completed_at',
        'pretty_json_data',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.annotate(
            follow_event_count=JSONArrayLength(
                JSONExtractPath('json_data', 'follow_events')
            ),
            unfollow_event_count=JSONArrayLength(
                JSONExtractPath('json_data', 'unfollow_events')
            ),
            tweet_create_event_count=JSONArrayLength(
                JSONExtractPath('json_data', 'tweet_create_events')
            ),
        ).order_by('-received_at')

    def follow_event_count(self, obj):
        return obj.follow_event_count

    def unfollow_event_count(self, obj):
        return obj.unfollow_event_count

    def tweet_create_event_count(self, obj):
        return obj.tweet_create_event_count

    follow_event_count.admin_order_field = 'follow_event_count'
    unfollow_event_count.admin_order_field = 'unfollow_event_count'
    tweet_create_event_count.admin_order_field = 'tweet_create_event_count'


    def pretty_json_data(self, instance):
        """Function to display pretty version of our data"""
        response = json.dumps(instance.json_data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StatusChoiceFilter(admin.SimpleListFilter):
    title = ('Status')

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('co', ('Completed')),
            ('ca', ('Cancelled')),
            ('pe', ('Pending')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'co':
            return queryset.filter(status='co')
        if self.value() == 'ca':
            return queryset.filter(status='ca')
        if self.value() == 'pe':
            return queryset.filter(status='pe')


@admin.register(TweetTextCompilation)
class TweetTextCompilationAdmin(admin.ModelAdmin):
    date_hierarchy = 'requested_at'
    list_display = (
        'id', 'user', 'requested_at', 'completed_at', 'status'
    )
    list_filter = (
        'init_tweet_deleted', StatusChoiceFilter,
    )
    readonly_fields = list_display + (
        'pretty_init_tweet_json', 'pretty_final_tweet_json', 'text'
    )
    search_fields = ['id', 'user__screen_name', 'user__name', 'user__location']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.annotate(
            status=Case(
                When(completed_at__isnull=False,then=Value('co')),
                When(init_tweet_deleted=True,then=Value('ca')),
                default=Value('pe'),
                output_field=CharField(),
            )
        ).order_by('-requested_at')

    def status(self, obj):
        if obj.status == 'co':
            return 'Completed'
        if obj.status == 'ca':
            return 'Cancelled'
        if obj.status == 'pe':
            return 'Pending'

    status.admin_order_field = 'status'


    def pretty_init_tweet_json(self, instance):
        """Function to display pretty version of our data"""
        response = json.dumps(instance.init_tweet_json, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    def pretty_final_tweet_json(self, instance):
        """Function to display pretty version of our data"""
        response = json.dumps(instance.final_tweet_json, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_follow_at'
    list_display = (
        'id', 'name', 'screen_name', 'location', 'last_follow_at',
        'completed_request_count', 'pending_request_count'
    )
    readonly_fields = (
        'id', 'name', 'screen_name', 'location', 'last_follow_at', 'pretty_json_data'
    )
    search_fields = ['id', 'name', 'screen_name', 'location']
    # is currently a follower?

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.annotate(
            completed_request_count=Count(
                'compilations', filter=Q(compilations__completed_at__isnull=True)
            ),
            pending_request_count=Count(
                'compilations', filter=Q(compilations__completed_at__isnull=False)
            ),
        ).order_by('-last_follow_at')

    def completed_request_count(self, obj):
        return obj.completed_request_count

    def pending_request_count(self, obj):
        return obj.pending_request_count

    completed_request_count.admin_order_field = 'completed_request_count'
    pending_request_count.admin_order_field = 'pending_request_count'

    def pretty_json_data(self, instance):
        """Function to display pretty version of our data"""
        response = json.dumps(instance.json_data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
