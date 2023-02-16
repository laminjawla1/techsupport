from django import forms
from django.contrib.auth.models import User
from .models import Account


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['image']
