from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'OWNER'


class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'RENTER'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
