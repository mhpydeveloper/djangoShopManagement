from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.core.exceptions import ValidationError


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_keeper = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    objects = UserManager()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email', 'full_name']

    def __str__(self):
        return f'{self.full_name} - {self.username}'

    def clean(self):
        # check if only one of the boolean fields is True
        if sum([self.is_keeper, self.is_seller, self.is_admin]) != 1:
            raise ValidationError("only one must be True(cadmin,keeper,seller)")

    @property
    def is_staff(self):
        return self.is_admin
