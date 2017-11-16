from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from rest_framework.authtoken.models import Token


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        super().create_superuser(age=30, *args, **kwargs)

    def create_facebook_user(selfself, facebook_user_id):
        pass

class User(AbstractUser):
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    CHOICE_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(
        max_length=1,
        choices=CHOICE_USER_TYPE
    )
    img_profile = models.ImageField(
        upload_to='user',
        blank=True
    )
    age = models.IntegerField('나이')

    like_posts = models.ManyToManyField(
        'post.Post',
        related_name='like_users',
        blank=True,
        verbose_name='좋아요 누른 포스트 목록'
    )

    # 내가 a를 follow 한다
    #     나는 a의 follower며
    #     a는 나의 following_user이다
    # 나를 follow하고 있는 사람 목록은
    #     follower
    # 내가 follow하고 있는 사람 목록은
    #     following

    # 내가 팔로우하고 있는 유저 목록
    following_user = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relation',
        related_name='followers'
    )

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    @property
    def token(self):
        return Token.objects.get_or_create(user=self)[0].key

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        relation, relation_created = self.following_user_relations.get_or_create(to_user=user)
        if relation_created:
            return True
        relation.delete()
        return False

        # if user in self.following_users.all():
        #     Relation.objects.filter(
        #         from_user=self,
        #         to_user=user,
        #     ).delete()
        # else:
        #     Relation.objecs.create(
        #         from_user=self,
        #         to_user=user,
        #     )
        #     self.following_user_relations.create(to_user=user)


class Relation(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user_relations'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations'
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: {self.from_user.username}, ' \
               f'to: {self.to_user.username})'
