from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'title', 'email', 'role', 'is_blocked')
    list_display_links = ('id', 'username')


admin.site.register(User, CustomUserAdmin)
