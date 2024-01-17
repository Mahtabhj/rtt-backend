from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rttorganization.models.models import Organization


class PublicAPIAuthenticationMiddleware(MiddlewareMixin):
    """The responsibility of this middleware is to authentication public api using key & secret
    and store some information for valid Public API.
    A valid public_api has two mandatory HEADER data: [01] key, [02] secret."""

    def process_request(self, request):
        """
        If the key and secret exist then using the
        key and secret try to find out a valid organization. After that inject the info of that organization in
        'request.public_api'
        """
        key = request.META.get('HTTP_KEY', None)
        secret = request.META.get('HTTP_SECRET', None)
        inject_info = {
            'has_access': False
        }
        if key and secret:
            organization = Organization.objects.filter(public_api_key=key, public_api_secret=secret).first()
            if organization:
                inject_info = {
                    'has_access': True,
                    'organization_id': organization.id
                }
        request.public_api = SimpleLazyObject(lambda: inject_info)
