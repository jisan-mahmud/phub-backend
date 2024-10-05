from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a snippet to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for any user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow write access only to the owner of the snippet
        return obj.user == request.user