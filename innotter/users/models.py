from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User - admin/moderator/user"""

    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True, max_length=200)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username
