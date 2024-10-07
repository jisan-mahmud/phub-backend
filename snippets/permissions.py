from rest_framework import permissions

class SnippetPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.visibility == 'public':
                return True
            
            if obj.visibility == 'unlisted':
                return True 

            if obj.visibility == 'private' and obj.user != request.user:
                return False
        
        return obj.user == request.user
