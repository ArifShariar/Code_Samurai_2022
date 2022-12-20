from django.contrib.auth.forms import UserCreationForm

from .models import *
from django import forms


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'Username', 'required': 'true'}
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'First Name', 'required': 'true'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder': 'Last Name', 'required': 'true'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder': 'Email', 'required': 'true'}
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Password', 'required': 'true'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm Password', 'required': 'true'}

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs = {'class': 'form-control', 'placeholder': 'User Type', 'required': 'true'}

    class Meta:
        model = Profile
        fields = ['user_type']
