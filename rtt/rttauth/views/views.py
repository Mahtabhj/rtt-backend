import uuid

from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rttauth.models.models import UserInvite, FailedLoginAttempt, PasswordReset
from rttauth.serializers.auth_serializers import UserSerializer, CreateUserSerializer, UserDetailSerializer, \
    MeDetailSerializer, ChangePasswordSerializer, InvitedUserSerializer, UpdateUserSerializer
from rttauth.services.user_service import UserService
from rttcore.permissions import IsOrganizationAdmin, is_admin_or_superuser
from rttorganization.models.models import Organization, Subscription
from rttorganization.serializers.serializers import OrganizationSerializer
from rttsubstance.models import PrioritizationStrategy
from rttdocumentManagement.services.quota_limit_service import QuotaLimitService

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    """
    Docs: https://chemycal.atlassian.net/browse/RTT-8?focusedCommentId=10841
    01. Failed login attempts: we could create a table to record these with
    timestamp and then the admin can see them in the django admin
    02. Password expire: we need to be able to see when a password was set (timestamp).
    If the user tries to log in after password expiration days, the system should ask 
    the user to set a new password (to be understood if we can redirect him to the new 
    password frontend screen same as when user forgot password and already clicked 
    on a link to reset)
    """
    def get_authenticate_header(self, request):
        try:
            user_name = request.data.get('username', None)
            user = User.objects.filter(username=user_name).first()
            if user is not None:
                create = FailedLoginAttempt.objects.create(user=user)
        except Exception as ex:
            print(ex)
        return super().get_authenticate_header(request)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            logged_in_length = (timezone.now() - serializer.user.last_pass_created_timestamp).days
            organization = Organization.objects.filter(id=serializer.user.organization_id).first()
            if organization.password_expiration != 0 and logged_in_length > organization.password_expiration:
                password_reset = PasswordReset.objects.create(user=serializer.user, code=uuid.uuid4().hex)
                serializer = None
                return Response({'message': 'Your password has expired. Please create a new password.',
                                 'code': password_reset.code},
                                status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_classes = {
        'list': UserDetailSerializer,
        'retrieve': UserDetailSerializer,
        'create': CreateUserSerializer,
        'update': UpdateUserSerializer,
        'partial_update': UpdateUserSerializer,
    }
    default_serializer_class = UserSerializer
    lookup_field = 'id'
    user_service = UserService()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsOrganizationAdmin]
        elif self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(UserViewSet, self).get_permissions()

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        organization_id = self.request.GET.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(organization_id=int(organization_id))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(UserDetailSerializer(page, many=True).data)
        else:
            serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        data = request.data
        is_admin = request.data.get('is_admin', False)
        if is_admin and not is_admin_or_superuser(request):
            data['is_admin'] = False
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            queryset = serializer.save()
            serializer = UserDetailSerializer(queryset)
            self.user_service.update_invited_user_status(serializer.data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = CreateUserSerializer(self.object, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         password = request.data.get('password', None)
    #         if password and is_staff_or_superuser(request):
    #             self.object.set_password(password)
    #         self.object.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        user = self.get_object()
        if request.user.is_superuser:
            user.delete()
        else:
            if request.user.is_admin and request.user.organization_id == user.organization_id:
                user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersMeApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = MeDetailSerializer(request.user, context={'request': request})
        data = serializer.data
        organization_id = request.user.organization_id
        current_time = datetime.now()
        active_substance_module_qs = Subscription.objects.filter(
            organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_substance_module=True).exists()
        active_limits_management_module_qs = Subscription.objects.filter(
            organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_limits_management_module=True).exists()
        active_task_management_module_qs = Subscription.objects.filter(
            organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_task_management_module=True).exists()
        substance_prioritization_strategy_qs = PrioritizationStrategy.objects.filter(
            organization=organization_id).exists()
        active_reports_module_qs = Subscription.objects.filter(
            organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_reports_module=True).exists()
        active_document_module_qs = Subscription.objects.filter(
            organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_document_module=True).exists()

        data['active_substance_module'] = True if active_substance_module_qs else False
        data['active_limits_management_module'] = True if active_limits_management_module_qs else False
        data['active_task_management_module'] = True if active_task_management_module_qs else False
        data['has_substance_prioritization_strategy'] = True if substance_prioritization_strategy_qs else False
        data['active_reports_module'] = True if active_reports_module_qs else False
        data['active_document_module'] = True if active_document_module_qs else False
        quota_limit_service = QuotaLimitService(organization_id)
        size_of_all_documents = quota_limit_service.get_quota_usage()
        max_quota_for_all_documents, max_quota_for_one_document = quota_limit_service.get_quota_limit()
        data['document_management'] = {
            "organization_limit": max_quota_for_all_documents,
            "single_upload_limit": max_quota_for_one_document,
            "total_usage": size_of_all_documents
        }

        return Response(data, status=status.HTTP_200_OK)


class OrganizationUsersApiView(APIView):
    permission_classes = [IsOrganizationAdmin]

    @staticmethod
    def get(request):
        organization_id = request.user.organization_id
        users = User.objects.filter(organization_id=organization_id)
        invited_users = UserInvite.objects.filter(status='pending', organization_id=organization_id)
        user_serializer = UserDetailSerializer(users, many=True)
        invited_users_serializer = InvitedUserSerializer(invited_users, many=True)
        org_users = user_serializer.data + invited_users_serializer.data
        return Response(status=status.HTTP_200_OK, data=org_users)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeOrganizationUserPassword(APIView):
    @staticmethod
    def put(request):
        try:
            data = request.data
            user = User.objects.filter(id=data.get('id')).first()
            if request.user.is_superuser and data.get('password') is not None:
                user.set_password(data.get('password'))
                user.save()
                return Response({'data': 'Ok'}, status=status.HTTP_200_OK)
            else:
                return Response({'data': 'Not changed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_admin:
            organization = Organization.objects.filter(id=self.object.organization_id).first()
            if organization:
                organization_serializer = OrganizationSerializer(organization, data=request.data, partial=True)
                if organization_serializer.is_valid():
                    organization_serializer.save()
        user_serializer = self.get_serializer(self.object, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserRole(generics.UpdateAPIView):
    serializer_class = UserDetailSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('id')).first()
        errors = None
        if self.request.user.is_admin and self.request.user.organization_id == user.organization_id:
            serializer = UserDetailSerializer(user, data={'is_admin': request.data.get('is_admin')}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class InviteUsersApiView(APIView):
    permission_classes = [IsOrganizationAdmin]
    user_service = UserService()

    def get(self, request):
        email = request.GET.get('email', None)
        message = 'User already exist this email'
        if email:
            user = User.objects.filter(email=email).first()
        else:
            message = "Email Should not be null"
            user = " "
        if not user:
            code = uuid.uuid4().hex
            organization_name = request.user.organization.name
            self.user_service.save_invite_user(email, code, request.user)
            self.user_service.send_invitation_email(email, code, organization_name)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': message
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CheckUserInvitationCodeApiView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        code = request.GET.get('code', None)
        user = UserInvite.objects.filter(code=code).first()
        if user:
            organization = {'id': user.organization.id, 'name': user.organization.name, 'email': user.email}
            return Response(organization, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid code'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CreateUserApiView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer
    model = User
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_admin:
            organization = Organization.objects.filter(id=self.object.organization_id).first()
            if organization:
                organization_serializer = OrganizationSerializer(organization, data=request.data, partial=True)
                if organization_serializer.is_valid():
                    organization_serializer.save()
        user_serializer = self.get_serializer(self.object, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
