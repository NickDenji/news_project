from rest_framework.permissions import BasePermission


class IsReader(BasePermission):
    """
    Custom permission to allow access only to users with the 'reader' role.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "reader"


class IsJournalist(BasePermission):
    """
    Allows access only to users with the journalist role.
    """

    def has_permission(self, request, view):
        return request.user.role == "journalist"


class IsEditor(BasePermission):
    """
    Allows access only to users with the editor role.
    """

    def has_permission(self, request, view):
        return request.user.role == "editor"


class IsEditorOrJournalist(BasePermission):
    """
    Allows access to editors and journalists.
    """

    def has_permission(self, request, view):
        return request.user.role in ["editor", "journalist"]
