from rest_framework import permissions

# Custom permission class to control access to snippets
class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        # Allow access if the request is using a safe method (e.g., GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow access if the user is authenticated
        if request.user.is_authenticated:
            return True
        
        # Otherwise, deny access (for non-authenticated users making unsafe requests)
        return False

    # Custom object-level permission for snippets
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user