from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
        Allows access only to manager users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_manager

class IsTeller(BasePermission):
    """
        Allows access only to tellers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_teller


class IsCustomer(BasePermission):
    """
        Allows access only to customers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_customer
