from rest_framework import permissions
from rest_framework.decorators import permission_classes


class IsModer(permissions.BasePermission):
    message = "Adding customers not allowed."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moders").exists()


class IsOwner(permissions.BasePermission):
    message = "Вы можете работать только со своими объектами"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser
