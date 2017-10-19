from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        # cleaned_data = super().clean() super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = authenticate(
            username=username,
            password=password
        )
        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials'
            )
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        django_login(request, self.user)


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already exists')
        return data

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Password1 and Password2 not equal')
        return password2

    def clean(self):
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data  # 클린메서드를 return 할 수도 있고 안 할 수도 있다.

    def _signup(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        return User.objects.create_user(
            username=username,
            password=password
        )
