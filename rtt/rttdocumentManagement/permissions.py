from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class HasDocManagementCommentEditPermission(BasePermission):
    message = "This user doesn't have the permission to edit the comment"
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.commented_by_id:
            return True
        return False

class IsDocManagementEditorSameOrdPermission(BasePermission):
    message = "User from different organization doesn't have the permission to edit"
    def has_object_permission(self, request, view, obj):
        user_object = User.objects.filter(id=obj.uploaded_by_id).first()
        doc_management_org_id = user_object.organization_id
        if request.user.organization_id == doc_management_org_id:
            return True
        return False
