from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Check if the user role is admin"""

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModerRole(permissions.BasePermission):
    """Check if the user role is moderator"""

    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsUserRole(permissions.BasePermission):
    """Check if the user role is user"""

    def has_permission(self, request, view):
        return request.user.role == 'user'
