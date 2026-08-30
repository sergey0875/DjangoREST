from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """ Проверяет является ли пользователь модератором"""

    def has_permission(self, request, view):
         if not (request.user and request.user.is_authenticated):
               return False

         return request.user.groups.filter(name='Moderator').exists()




class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Проверяет является ли пользователь владельцем
    """

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False