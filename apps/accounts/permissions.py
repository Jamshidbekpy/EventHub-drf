from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_organizer_pending == True