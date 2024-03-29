from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "page", "reply_to", "updated_at")
    list_display_links = ("id", "content")


admin.site.register(Post, PostAdmin)
