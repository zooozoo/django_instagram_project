from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from ..forms import SignupForm, LoginForm

User = get_user_model()

__all__ = (
    'login',
    'logout_view',
    'signup',
)


def login(request):
    next_path = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # is_valid 과정에서 clean메서드를 통해 사용자가 인증된다.
            form.login(request)  # form에 login 함수를 만들고 그걸 이용해서 login
            if next_path:
                return redirect(next_path)
            return redirect('post:post_list')
    else:
        form = LoginForm()
    context = {
        'login_form': form,
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
    }
    return render(request, 'member/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user, backend='django.contrib.auth.backends.ModelBackends')
            return redirect('post:post_list')
    else:
        form = SignupForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'member/signup.html', context)
