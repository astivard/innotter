from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User - admin/moderator/user"""

    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    __original_user_role = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_user_role = self.role

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role != self.__original_user_role and self.role == 'admin':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)
        self.__original_user_role = self.role


