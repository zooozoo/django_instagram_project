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
