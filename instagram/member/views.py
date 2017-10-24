from pprint import pprint
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login as django_login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import SignupForm, LoginForm

User = get_user_model()


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
        form = SignupForm(request.POST, request.files)
        if form.is_valid():
            form.save()
            return redirect('post:post_list')
    else:
        form = SignupForm()
    context = {
        'signup_form': form,
    }
    return render(request, 'member/signup.html', context)


def facebook_login(request):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: str

    class DebugTokenInfo(NamedTuple):
        app_id: str
        application: str
        expires_at: int
        is_valid: bool
        issued_at: int
        scopes: str
        type: str
        user_id: str

    class UserInfo():
        def __init__(self, data):
            self.id = data['id']
            self.email = data.get('email', '')
            self.url_picture = data['picture']['data']['url']

    app_id = settings.FACEBOOK_APP_ID
    app_secret_code = settings.FACEBOOK_APP_SECRET_CODE
    app_access_token = f'{app_id}|{app_secret_code}'
    code = request.GET.get('code')

    def get_access_token(code):
        redirect_uri = '{scheme}://{host}{relative_url}'.format(
            scheme=request.scheme,
            host=request.META['HTTP_HOST'],
            relative_url=reverse('member:facebook-login')
        )
        url_access_token = 'https://graph.facebook.com/v2.10/oauth/access_token'
        params_access_token = {
            'client_id': app_id,
            'redirect_uri': redirect_uri,
            'client_secret': app_secret_code,
            'code': code
        }
        response = requests.get(url_access_token, params_access_token)
        return AccessTokenInfo(**response.json())

    def get_debug_token_info(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        params_debug_token = {
            'input_token': token,
            'access_token': app_access_token,
        }
        response = requests.get(url_debug_token, params_debug_token)
        return DebugTokenInfo(**response.json()['data'])

    access_token_info = get_access_token(code)
    access_token = access_token_info.access_token
    debug_token_info = get_debug_token_info(access_token)

    user_info_fields = {
        'id',
        'name',
        'picture',
        'email',
    }
    url_graph_user_info = 'https://graph.facebook.com/me'
    params_graph_user_info = {
        'fields': ','.join(user_info_fields),
        'access_token': access_token,
    }
    response = requests.get(url_graph_user_info, params_graph_user_info)
    result = response.json()
    user_info = UserInfo(data=result)

    # 페이스북으로 가입한 유저의username
    # fb_<facebook_user_id>
    username = f'fb_{user_info.id}'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        django_login(request, user)
    else:
        user = User.objects.create_user(
            user_type=User.USER_TYPE_FACEBOOK,
            username=username,
            age=0
        )
    django_login(request, user)
    return HttpResponse(result.items())
