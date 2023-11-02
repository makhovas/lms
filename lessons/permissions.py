from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwnerorStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True

        return False
