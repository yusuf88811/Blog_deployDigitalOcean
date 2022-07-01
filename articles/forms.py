from django.core.mail import send_mail
from django.forms import ModelForm
from django import forms
from .models import Comment


class CommentForm(ModelForm):
    # author = forms.
    # comment = forms.CharField()
    # articles = forms.CharField()

    class Meta:
        model = Comment
        fields = ["comment"]






