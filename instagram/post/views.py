from django.http import HttpResponse
from django.shortcuts import render

from post.form import PostForm
from post.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            post = Post.objects.create(photo=form.cleaned_data['photo'])
            return HttpResponse(f'<img src="{post.photo.url}">')
    else:
        form = PostForm()  # GET요청의 경우, 빈 PostForm인스턴스를 생성해서 템플릿에 전달
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)

def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    context = {
        'post':post,
    }
    return render(request, 'post/post_detail.html', context)
