from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rttcore.permissions import IsActiveLimitsManagementModule
from rttlimitManagement.models import LimitAttribute
from rttlimitManagement.serializers import LimitAttributeIdNameSerializer


class LimitAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LimitAttribute.objects.all()
    serializer_class = LimitAttributeIdNameSerializer
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    def get_queryset(self):
        regulatory_framework = self.request.GET.get('regulatory_framework', None)
        regulation = self.request.GET.get('regulation', None)
        if regulation:
            return self.queryset.filter(regulation_limit_attribute__regulation=regulation)
        elif regulatory_framework:
            return self.queryset.filter(regulation_limit_attribute__regulatory_framework=regulatory_framework)
        return self.queryset
