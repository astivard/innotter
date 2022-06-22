from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Checks if the user role is admin"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin'

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModerRole(permissions.BasePermission):
    """Checks if the user role is moderator"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'

    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsUserRole(permissions.BasePermission):
    """Checks if the user role is user"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'user'

    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsBlockedUser(permissions.BasePermission):
    """Checks if the user is blocked"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_blocked

    def has_permission(self, request, view):
        return request.user.is_blocked
