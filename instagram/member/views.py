from django.contrib.auth.models import User
from django.shortcuts import render

def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, password)
