from datetime import datetime
from rttorganization.models.models import Subscription
from rest_framework.permissions import BasePermission


class IsSuperUserOrStaff(BasePermission):
    """The IsSuperUserOrStaff permission class will deny permission to any user, unless user.is_superuser or
    user.is_staff is True in which case permission will be allowed."""
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))


class IsOrganizationAdmin(BasePermission):
    """ Allows access only to organization admin."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


def is_staff_or_superuser(request):
    """ Check is user staff or superuser."""

    return bool(request.user and (request.user.is_staff or request.user.is_superuser))


def is_admin_or_superuser(request):
    """ Check is user organization admin or superuser."""

    return bool(request.user and request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser))


class IsActiveSubstanceModule(BasePermission):
    """ users having SubstanceModule Subscription can access for a particular Organization. """

    def has_permission(self, request, view):
        if request.user:
            organization_id = request.user.organization_id
            current_time = datetime.now()
            active_substance_module = Subscription.objects.filter(
                organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
                type__is_active_substance_module=True).exists()
            return active_substance_module
        return False


def has_substance_module_permission(organization_id):
    """organization_id will be given as parameter, have to return True if that organization has any active
    SubstanceModule Subscription or False otherwise."""
    current_time = datetime.now()
    active_substance_module = Subscription.objects.filter(
        organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
        type__is_active_substance_module=True).exists()
    return active_substance_module


class IsActiveLimitsManagementModule(BasePermission):
    """ users having LimitsManagementModule Subscription can access for a particular Organization. """

    def has_permission(self, request, view):
        if request.user:
            organization_id = request.user.organization_id
            current_time = datetime.now()
            active_limits_management_module = Subscription.objects.filter(
                organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
                type__is_active_limits_management_module=True).exists()
            return active_limits_management_module
        return False


class IsActiveTaskManagementModule(BasePermission):
    """ users having TaskManagementModule Subscription can access for a particular Organization. """

    def has_permission(self, request, view):
        if request.user:
            organization_id = request.user.organization_id
            current_time = datetime.now()
            active_task_management_module = Subscription.objects.filter(
                organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
                type__is_active_task_management_module=True).exists()
            return active_task_management_module
        return False


class IsActiveReportsModule(BasePermission):
    """ users having ReportsModule Subscription can access for a particular Organization. """

    def has_permission(self, request, view):
        if request.user:
            organization_id = request.user.organization_id
            current_time = datetime.now()
            active_reports_module = Subscription.objects.filter(
                organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
                type__is_active_reports_module=True).exists()
            return active_reports_module
        return False


def has_reports_module_permission(organization_id):
    """organization_id will be given as parameter, have to return True if that organization has any active
    ReportsModule Subscription or False otherwise."""
    current_time = datetime.now()
    active_reports_module = Subscription.objects.filter(
        organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
        type__is_active_reports_module=True).exists()
    return active_reports_module


class IsActiveDocumentManagementModule(BasePermission):
    """ users having DocumentManagementModule Subscription can access for a particular Organization. """

    def has_permission(self, request, view):
        if request.user:
            organization_id = request.user.organization_id
            current_time = datetime.now()
            active_document_management_module = Subscription.objects.filter(
                organization=organization_id, start_date__lte=current_time, end_date__gte=current_time,
                type__is_active_document_module=True).exists()
            return active_document_management_module
        return False
