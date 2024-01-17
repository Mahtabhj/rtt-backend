import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models, IntegrityError
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rttcore.models.models import BaseTimeStampedModel
from rttcore.services.exceptions import NotDeletable
from rttorganization.models.models import Organization

USER_STATUS_CHOICES = [
    ('created', 'Created'),
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('deleted', 'Deleted'),
]


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):
    name = CharField(_('Name of User'), blank=True, max_length=255)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.FileField(upload_to='media/user', blank=True, null=True)
    is_admin = models.BooleanField(_('Organization admin status'), default=False)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='created')

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='organization_user')

    objects = CustomUserManager()
    last_pass_created_timestamp = models.DateTimeField(_('last password changed timestamp'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def delete(self, **kwargs):
        try:
            super(User, self).delete()
        except IntegrityError:
            raise NotDeletable

    def set_password(self, raw_password, **kwargs):
        if self.username:
            self.last_pass_created_timestamp = timezone.now()
            # self.save()
        super().set_password(raw_password)


class UserInvite(BaseTimeStampedModel):
    email = models.EmailField()
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='pending')
    code = models.CharField(max_length=100)

    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='user_invite_user')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='user_invite_organization')

    def __str__(self):
        return str(self.email)


class PasswordReset(BaseTimeStampedModel):
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_user')


class FailedLoginAttempt(BaseTimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='failed_login_attempt_user')
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)

    def __str__(self):
        return f'Failed login attempt by {self.user.username}'
