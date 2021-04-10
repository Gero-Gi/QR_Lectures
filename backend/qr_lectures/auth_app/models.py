from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    is_active = models.BooleanField(default=True)

    is_professor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_superuser


class UserDevice(models.Model):
    user = OneToOneField(User, on_delete=CASCADE)
    udi = models.CharField(max_length=16)

    def __str__(self):
        return self.udi

    def check_udi(self, udi):
        return self.udi == udi