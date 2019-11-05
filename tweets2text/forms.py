from django import forms
from django.forms import ModelForm, Textarea
from .models import TweetTextCompilation

class TextEditForm(forms.ModelForm):
    class Meta:
        model = TweetTextCompilation
        fields = [
            'text',
        ]
        widgets = {
            'text': Textarea(attrs={'cols': 273, 'rows': 30}),
        }
        labels = {
            'text': (''),
        }