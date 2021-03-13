import uuid
from django.apps import apps
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from api.managers.user_manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, default='')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=EMPLOYEE)
    objects = UserManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'api'

    def __str__(self):
        return self.email
    
    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_email(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.username
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)
