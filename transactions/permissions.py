from rest_framework.permissions import BasePermission


class IsAdminAndActivated(BasePermission):
    """
        Allows access only to authenticated, activated and admin users.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_activated and user.is_staff


class IsAuthenticatedAndActivated(BasePermission):
    """
        Allows access only to authenticated and activated users.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_activated
