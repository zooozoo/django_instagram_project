from rest_framework import generics, permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer
from .models import Post


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )

class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_pk'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.like_posts.filter(pk=instance.pk):
            user.like_posts.remove(instance)
            like_status = False
        else:
            user.like_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status
        }
        return Response(data)