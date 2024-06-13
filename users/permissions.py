from rest_framework import permissions

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'field_agent'

class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'supervisor'

class IsReviewer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'reviewer'