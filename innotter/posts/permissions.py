from rest_framework import permissions


class IsAdminOrModeratorRole(permissions.BasePermission):
    """Check if the user role is admin or moderator"""

    def has_permission(self, request, view):
        return request.user.role in ('admin', 'moderator')


class IsUserPageOwner(permissions.BasePermission):
    """Check if the page owned by user"""

    def has_object_permission(self, request, view, obj):
        return obj.page.owner == request.user

