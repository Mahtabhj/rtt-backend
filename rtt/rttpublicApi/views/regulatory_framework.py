from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttpublicApi.permissions import IsPublicApiAuthorized
from rttregulation.documents import MilestoneDocument


class RegulatoryFrameworkApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def get(self, request):
        organization_id = request.public_api.get('organization_id', None)
        framework_ids = request.GET.get('ids', [])
        limit = int(request.GET.get('limit', 10))
        skip = int(request.GET.get('skip', 0))

        results = []
        regulatory_framework_search = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            organization_id).sort('id')
        if framework_ids:
            framework_ids = framework_ids.split(',')
            regulatory_framework_search = regulatory_framework_search.filter('terms', id=framework_ids)

        count = regulatory_framework_search.count()
        regulatory_framework_search = regulatory_framework_search[skip:limit + skip]

        for framework in regulatory_framework_search:
            results.append(self.__get_framework_object(framework))
        response_data = {
            'count': count,
            'results': results
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def __get_framework_object(self, framework_document):
        framework_obj = {
            'id': framework_document.id,
            'name': framework_document.name,
            'description': framework_document.description,
            'last_update': framework_document.modified,
            'regions': [{'id': region.id, 'name': region.name} for region in framework_document.regions],
            'milestones': self.__get_milestones(framework_document.id, is_regulation=False),
            'regulations': [],
        }
        for regulation in framework_document.regulation_regulatory_framework:
            regulation_obj = {
                "id": regulation.id,
                "name": regulation.name,
                "description": regulation.description,
                "type": {
                    "id": regulation.type.id,
                    "name": regulation.type.name
                },
                "regions": framework_obj['regions'],
                "last_update": regulation.modified,
                "milestones": self.__get_milestones(regulation.id)
            }
            framework_obj['regulations'].append(regulation_obj)
        return framework_obj

    @staticmethod
    def __get_milestones(r_or_rf_id, is_regulation=True):
        if is_regulation:
            milestone_list = MilestoneDocument.search().filter('match', regulation__id=r_or_rf_id)
        else:
            milestone_list = MilestoneDocument.search().filter('match', regulatory_framework__id=r_or_rf_id)

        milestones = []
        for milestone in milestone_list:
            milestones.append({
                "id": milestone.id,
                "name": milestone.name,
                "description": milestone.description,
                "from_date": milestone.from_date,
                "to_date": milestone.to_date,
                "type": {
                    "id": milestone.type.id,
                    "name": milestone.type.name
                },
                "documents": [
                    {
                        "id": document.id,
                        "title": document.title,
                        "link": document.attachment
                    } for document in milestone.documents
                ],
                "urls": [
                    {
                        "id": url.id,
                        "title": url.description,
                        "link": url.text
                    } for url in milestone.urls
                ]
            })
        return milestones
