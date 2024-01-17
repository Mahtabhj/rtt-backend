from rttauth.models.models import UserInvite
from rttcore.services.email_service import mail_send, send_mail_via_mailjet_template
from django.conf import settings


class UserService:

    @staticmethod
    def save_invite_user(email, code, user):
        user_invite = UserInvite(
            email=email,
            code=code,
            invited_by=user,
            organization=user.organization
        )
        user_invite.save()

    @staticmethod
    def send_invitation_email(email_to, code, organization_name):
        base_url = settings.SITE_BASE_URL
        subject = 'Regulatory Tracking Platform | Invitation to join'
        variables_dict = {
            "organization_name": organization_name,
            "invitation_link": f'''{base_url}registration?code={code}'''
        }
        template_id = settings.MAILJET_SEND_INVITATION_TEMPLATE_ID
        return send_mail_via_mailjet_template(email_to, template_id, variables_dict=variables_dict)

    @staticmethod
    def send_password_reset_email(email_to, username, code):
        base_url = settings.SITE_BASE_URL
        subject = 'Regulatory Tracking Platform | Password reset'
        variables_dict = {
            "name": username,
            "resetlink": f'''{base_url}password-reset?code={code}'''
        }
        template_id = settings.MAILJET_RESET_PASSWORD_TEMPLATE_ID
        return send_mail_via_mailjet_template(email_to, template_id, variables_dict=variables_dict)

    @staticmethod
    def update_invited_user_status(user):
        organization_id = user['organization']['id']
        invited_user = UserInvite.objects.filter(
            status='pending',
            email=user['email'],
            organization_id=organization_id).first()
        if invited_user:
            invited_user.status = 'accepted'
            invited_user.save()
