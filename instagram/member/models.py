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
    age = models.IntegerField()

    objects = UserManager()

    # REQUIRED_FIELDS =  AbstractUser.REQUIRED_FIELDS + ['age']
