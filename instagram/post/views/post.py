from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from member.decorators import login_required
from post.forms import PostForm, CommentForm
from post.models import Post

__all__ = (
    'post_list',
    'post_create',
    'post_detail',
    'post_delete',
    'post_like_toggle',
)


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    if not request.user.is_authenticated():
        return redirect('member:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_list')
    else:
        form = PostForm()  # GET요청의 경우, 빈 PostForm인스턴스를 생성해서 템플릿에 전달
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_detail(request, post_pk):
    # post = Post.objects.get(pk=post_pk)
    # 겟을 했을 때 pk번호가 유효하지 않으면
    # 500번대 서버 에러메시지를 보여주게 되는데
    # 404 메시지를 보여주는게 좀더 정확하기 때문에 아래의 코드로 대체힌다.
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied
    return HttpResponse('로그인 후 이용하세요')


@login_required
def post_like_toggle(request, post_pk):
    next_path = request.GET.get('next')
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    filtered_like_posts = user.like_posts.filter(pk=post.pk)

    if filtered_like_posts.exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)

    if next_path:
        return redirect(next_path)
    return redirect('post:post_detail', post_pk=post_pk)
