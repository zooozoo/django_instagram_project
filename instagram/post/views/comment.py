from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from member.decorators import login_required
from post.forms import CommentForm
from post.models import Post, PostComment

__all__ = (
    'comment_create',
    'comment_delete',
)


@login_required
def comment_create(request, post_pk):
    if not request.user.is_authenticated():
        return redirect('member:login')
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            next = request.GET.get('next', '').strip()
            # post_list페이지 에서 댓글을 달더라도 post_create페이지로
            # 이동 하는 것이 아니라 post_list에서 바로 작성될 수 있도록 해주기 위해
            # 탬플릿의 form 태그에 get파라미터를 추가하고
            # 아래의 if 문으로 get 파라미터의 키 값인
            # next를 확인하해서 post_list로 리다이렉트 해준다.
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post_pk)


def comment_delete(request, comment_pk):
    comment = PostComment.objects.get(pk=comment_pk)
    if request.method == 'POST':
        if request.user == comment.author:
            comment.delete()
            return redirect('post:post_list')
    return HttpResponse('로그인이 필요합니다.')
