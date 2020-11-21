from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from website.models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1']

class profilepic(ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['profile_pic']