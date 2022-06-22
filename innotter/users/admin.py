from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "title", "email", "role", "is_blocked")
    list_display_links = ("id", "username")


admin.site.register(User, UserAdmin)
