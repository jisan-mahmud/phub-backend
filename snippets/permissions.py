from rest_framework import permissions

# Custom permission class to control access to snippets
class SnippetPermission(permissions.BasePermission):
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
        # Allow access for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # If the snippet is public, allow access
            if obj.visibility == 'public':
                return True
            
            # If the snippet is unlisted, allow access (it's not fully private but not public either)
            if obj.visibility == 'unlisted' and obj.user != request.user:
                return False 

            # If the snippet is private and the current user is not the owner, deny access
            if obj.visibility == 'private' and obj.user != request.user:
                return False

        # For unsafe methods (e.g., POST, PUT, DELETE), only allow the owner of the snippet
        return obj.user == request.user