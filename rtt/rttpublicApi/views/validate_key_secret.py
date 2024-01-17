from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rttpublicApi.permissions import is_key_secret_valid


class ValidateKeySecretApi(APIView):
    def post(self, request):
        key = request.data.get('key', None)
        secret = request.data.get('secret', None)
        is_valid = is_key_secret_valid(key, secret)
        if is_valid:
            response = {
                'code': 200,
                'message': 'key & secret is valid.'
            }
        else:
            response = {
                'code': 401,
                'message': 'key & secret is invalid.'
            }
        return Response(response, status=status.HTTP_200_OK if is_valid else status.HTTP_401_UNAUTHORIZED)
