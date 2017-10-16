from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from post.form import PostForm, CommentForm
from post.models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form
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
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            PostComment.objects.create(
                post=post,
                content=form.cleaned_data['content'],
            )
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post_detail', post_pk=post_pk)
