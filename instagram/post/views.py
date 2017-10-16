from django.http import HttpResponse
from django.shortcuts import render

from post.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)

def post_create(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
    elif request.method == 'GET':
        return render(request, 'post/post_create.html')