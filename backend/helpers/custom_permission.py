from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response

"""
PERMISSION CLASS FOR ALL APIS
"""


class APIKeyPermission(permissions.BasePermission):

    """
    To check if our API Token if present at every request or not.
    """

    def has_permission(self, request, view):
        api_key = request.META.get("HTTP_X_API_KEY", "")
        if api_key and api_key == settings.WEB_API_KEY:
            return True
        else:
            return False

    @property
    def message(self):
        return Response({"status": "error", "message": "Invalid Key"})