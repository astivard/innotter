from rest_framework import permissions

from users.models import User


class IsAdminRole(permissions.BasePermission):
    """Checks if the user role is admin"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.ADMIN

    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN


class IsModerRole(permissions.BasePermission):
    """Checks if the user role is moderator"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.MODERATOR

    def has_permission(self, request, view):
        return request.user.role == User.Roles.MODERATOR


class IsUserRole(permissions.BasePermission):
    """Checks if the user role is user"""

    def has_object_permission(self, request, view, obj):
        return request.user.role == User.Roles.USER

    def has_permission(self, request, view):
        return request.user.role == User.Roles.USER


class IsBlockedUser(permissions.BasePermission):
    """Checks if the user is blocked"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_blocked

    def has_permission(self, request, view):
        return request.user.is_blocked
