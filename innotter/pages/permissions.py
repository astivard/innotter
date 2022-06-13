from rest_framework import permissions


class IsPublicPage(permissions.BasePermission):
    """Check if the page is private"""

    def has_object_permission(self, request, view, obj):
        return not obj.is_private
