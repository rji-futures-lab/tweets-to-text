from django.urls import path
from . import views


app_name = 'tweets2text'
urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path(
        'compilation/<uuid:compilation_id>',
        views.plain_text_view, name='compilation',
    ),
    path('webhooks/twitter/', views.TwitterWebhook.as_view()),
]
