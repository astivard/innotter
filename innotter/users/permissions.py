from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return False
