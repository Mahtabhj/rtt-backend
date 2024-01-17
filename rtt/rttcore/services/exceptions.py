from rest_framework import status
from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _


class NotDeletable(APIException):
    status_code = status.HTTP_424_FAILED_DEPENDENCY
    default_detail = _('It has some dependent entry in db')
    default_code = 'not deletable'
