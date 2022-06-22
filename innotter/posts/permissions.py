from rest_framework import permissions


class IsUserPageOwner(permissions.BasePermission):
    """Checks if the page owned by user"""

    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.user
