import uuid

from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rttauth.models.models import PasswordReset
from rttauth.services.user_service import UserService

User = get_user_model()


class SendPasswordResetLinkApiView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """
        params:
            email: required=True
        """
        email = request.data.get('email', None)
        if not email:
            return Response({
                'message': 'email is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'message': 'No user found with this email!'
            }, status=status.HTTP_404_NOT_FOUND)

        password_reset = PasswordReset.objects.create(user=user, code=uuid.uuid4().hex)
        UserService().send_password_reset_email(user.email, user.username, password_reset.code)
        return Response({
            'message': 'Successfully email send with password reset link.'
        }, status=status.HTTP_200_OK)


class PasswordResetPostSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PasswordResetApiView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """
        params:
            code: required=True
            password: required=True
        """
        validation = PasswordResetPostSerializer(data=request.data)
        if not validation.is_valid():
            return Response(validation.errors, status=status.HTTP_400_BAD_REQUEST)
        data = validation.validated_data

        password_reset_request_obj: PasswordReset = PasswordReset.objects.filter(code=data.get('code'),
                                                                                 active=True).first()
        if not password_reset_request_obj:
            return Response({
                'message': 'Invalid reset code!'
            }, status=status.HTTP_403_FORBIDDEN)

        '''
        change password
        '''
        user = password_reset_request_obj.user
        user.set_password(data.get('password'))
        user.save()

        '''
        reset password code can use only 1 time.
        '''
        password_reset_request_obj.active = False
        password_reset_request_obj.save()

        return Response({
            'message': 'Password updated successfully'
        }, status=status.HTTP_200_OK)
