from rest_framework.permissions import BasePermission


class CityPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj in request.user.profile.cities.all()
