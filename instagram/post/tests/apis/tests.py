import filecmp
import io
import os
from random import randint

from django.conf import settings
from django.core.files import File
from django.urls import resolve
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIRequestFactory

from member.forms import User
from post.apis import PostList
from post.models import Post


class PostListviewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username, age=0)

    @staticmethod
    def create_post(author=None):
        Post.objects.create(author=author, photo=File(io.BytesIO()),)

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve_view_class(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(
            resolver_match.url_name,
            self.URL_API_POST_LIST_NAME)

        self.assertEqual(
            resolver_match.func.view_class,
            self.VIEW_CLASS)

    def test_get_post_list(self):
        user = self.create_user()
        num = randint(1, 20)
        for i in range(num):
            self.create_post(author=user)

        url = reverse(self.URL_API_POST_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), num)
        self.assertEqual(len(response.data), num)

        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_at', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

        response = self.client.get(self.URL_API_POST_LIST)
        self.assertEqual(len(response.data), num_posts)

    def test_create_post(self):
        user = self.create_user()
        self.client.force_authenticate(user=user)
        path = os.path.join(settings.STATIC_DIR, 'test', 'goat.png')

        with open(path, 'rb') as photo:
            response = self.client.post('/api/post/', {
                'photo': photo,
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.get(pk=response.data['pk'])

        self.assertTrue(filecmp.cmp(path, post.photo.file.name))

        print(path)
        print(post.photo.file.name)