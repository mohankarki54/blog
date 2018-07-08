from django import forms

from .models import Post, Comment, Feed
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('author','title', 'image' , 'text', )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }


class UserCreateForm(UserCreationForm):

    first_name = forms.CharField(max_length=25, required= True, help_text = 'Required')
    last_name = forms.CharField(max_length=30, required=True,help_text = 'Required')
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        fields = ("username",'first_name','last_name', "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ('url',)

        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'})
        }
