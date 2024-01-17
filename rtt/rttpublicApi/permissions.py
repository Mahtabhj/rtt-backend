from rest_framework.permissions import BasePermission

from rttorganization.models.models import Organization


class IsPublicApiAuthorized(BasePermission):
    """ Allows access only to public api."""

    def has_permission(self, request, view):
        return request.public_api and request.public_api.get('has_access', False)


def is_key_secret_valid(key, secret):
    is_valid = False
    if key and secret:
        organization = Organization.objects.filter(public_api_key=key, public_api_secret=secret).first()
        if organization:
            is_valid = True
    return is_valid
