from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user',
        blank=True
    )
    age = models.IntegerField('나이')

    like_post = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록'
    )

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'



        # REQUIRED_FIELDS =  AbstractUser.REQUIRED_FIELDS + ['age']
