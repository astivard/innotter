from rest_framework import permissions


class IsPrivatePage(permissions.BasePermission):
    """Checks if the page is private"""

    def has_object_permission(self, request, view, obj):
        return obj.is_private


class IsPageFollower(permissions.BasePermission):
    """Checks if the user is a follower of page"""

    def has_object_permission(self, request, view, obj):
        return obj.is_private and request.user in obj.followers.all()
