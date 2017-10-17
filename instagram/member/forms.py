from django import forms

__all__ = (
    'SignupForm',
)

class SignupForm():
    username = forms.CharField()
    password = forms.CharField()