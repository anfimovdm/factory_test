from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (
                view.action == 'complete_quiz'):
            return True
        return True if request.user and request.user.is_staff else False

