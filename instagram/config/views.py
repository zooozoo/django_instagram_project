from django.shortcuts import redirect


def redirect_post_list(request):
    return redirect('post:post_list')