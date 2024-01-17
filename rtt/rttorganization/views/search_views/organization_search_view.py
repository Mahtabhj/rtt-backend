from rest_framework import generics, permissions
from rttorganization.documents import OrganizationDocument
from rttorganization.serializers.serializers import OrganizationSerializer


class OrganizationApiView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = OrganizationDocument.search().query({
            "term": {
                "name": self.request.GET.get('search')
            }
        }).to_queryset()
        return queryset
