from rest_framework.permissions import BasePermission


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return True if request.user.is_staff else obj == request.user.profile
