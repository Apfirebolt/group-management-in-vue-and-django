from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.methods in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_superuser