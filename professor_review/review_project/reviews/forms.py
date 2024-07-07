from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        help_text="",  # Remove the help text
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,  # Prevent stripping leading/trailing whitespace
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


# Add this to your forms.py
from .models import Discussion, DiscussionReply
class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']

class DiscussionReplyForm(forms.ModelForm):
    class Meta:
        model = DiscussionReply
        fields = ['content']

