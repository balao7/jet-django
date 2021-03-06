from rest_framework.permissions import BasePermission

from jet_django import settings
from jet_django.utils.backend import project_auth


class HasProjectPermissions(BasePermission):
    token_prefix = 'Token '
    project_token_prefix = 'ProjectToken '

    def has_permission(self, request, view):
    #     return True
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return False

        if token[:len(self.token_prefix)] == self.token_prefix:
            token = token[len(self.token_prefix):]

            return project_auth(token)
        elif token[:len(self.project_token_prefix)] == self.project_token_prefix:
            token = token[len(self.project_token_prefix):]

            return project_auth(token)
        else:
            return False


class ModifyNotInDemo(BasePermission):

    def has_permission(self, request, view):
        if not settings.JET_DEMO:
            return True
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return False
        return True
