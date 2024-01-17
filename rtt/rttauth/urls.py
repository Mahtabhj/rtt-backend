from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from rttauth.views.password_reset_view import SendPasswordResetLinkApiView, PasswordResetApiView
from rttauth.views.views import UserViewSet, OrganizationUsersApiView, UsersMeApiView, ChangePasswordView, \
    UpdateUserView, MyTokenObtainPairView, UpdateUserRole, InviteUsersApiView, CheckUserInvitationCodeApiView, \
    ChangeOrganizationUserPassword

router = DefaultRouter()
router.register(r'users', UserViewSet)

app_name = 'users'

urlpatterns = [
                  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('users/me/', UsersMeApiView.as_view(), name='me_api'),
                  path('users/change-organization-user-password/', ChangeOrganizationUserPassword.as_view(),
                       name='change_organization_user_password'),
                  path('organization-users/', OrganizationUsersApiView.as_view(), name='organization_users'),
                  path('change-password/', ChangePasswordView.as_view(), name='change_password'),
                  path('update-user/', UpdateUserView.as_view(), name='update_user'),
                  path('update-role/', UpdateUserRole.as_view(), name='update_role'),
                  path('invite-user/', InviteUsersApiView.as_view(), name='invite_user'),
                  path('check-invitation-code/', CheckUserInvitationCodeApiView.as_view(),
                       name='check_invitation_code'),
                  path('send-password-reset-link/', SendPasswordResetLinkApiView.as_view(),
                       name='send_password_reset_link'),
                  path('password-reset/', PasswordResetApiView.as_view(),
                       name='password_reset'),
              ] + router.urls
