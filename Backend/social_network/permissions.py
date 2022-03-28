from rest_framework.permissions import BasePermission
from .models import Post


class UserPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        return bool(request.user and request.user == obj.author)
