from django.contrib import admin

from pages.models import Page, Tag


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uuid', 'owner', 'is_private')
    list_display_links = ('id', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Page, PageAdmin)
admin.site.register(Tag, TagAdmin)
