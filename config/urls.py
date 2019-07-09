"""
Django project URL configuration.

The `urlpatterns` list routes URLs to views.

For more information, check out
https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweets2text.urls')),
]
