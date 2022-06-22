from django.contrib import admin

from pages.models import Page, Tag


class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "uuid", "is_blocked", "is_private", "owner")
    list_display_links = ("id", "name")


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


admin.site.register(Page, PageAdmin)
admin.site.register(Tag, TagAdmin)
