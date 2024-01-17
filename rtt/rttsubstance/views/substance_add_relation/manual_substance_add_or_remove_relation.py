from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsSuperUserOrStaff
from rttsubstance.models import Substance
from rttregulation.models.models import Regulation, RegulatoryFramework, RegulationMilestone

logger = logging.getLogger(__name__)


class ManualSubstanceAddOrRemoveRelation(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'substances': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of substance ID',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='input regulation_id'),
            'regulatory_framework_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='input '
                                                                                             'regulatory_framework_id'),
            'milestone_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='input milestone_id'),
            'action': openapi.Schema(type=openapi.TYPE_STRING, description='send add/remove/remove-all keyword')
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-876 --> add manually
        doc: https://chemycal.atlassian.net/browse/RTT-885 --> remove
        doc: https://chemycal.atlassian.net/browse/RTT-885?focusedCommentId=12328 ---> remove all
        """
        try:
            regulation_id = request.data.get('regulation_id', None)
            regulatory_framework_id = request.data.get('regulatory_framework_id', None)
            milestone_id = request.data.get('milestone_id', None)
            substances = request.data.get('substances', None)
            action = request.data.get('action', None)
            param_count = 0
            if regulation_id:
                param_count += 1
            if regulatory_framework_id:
                param_count += 1
            if milestone_id:
                param_count += 1
            if param_count != 1:
                return Response({"message": "regulation_id OR regulatory_framework_id OR milestone_id must be sent"},
                                status=status.HTTP_400_BAD_REQUEST)
            if not action or action not in ['add', 'remove', 'remove-all']:
                return Response({"message": "action must be defined. send add, remove or remove-all keyword"},
                                status=status.HTTP_400_BAD_REQUEST)

            if not substances and action != 'remove-all':
                return Response({"message": "substances must be sent"}, status=status.HTTP_400_BAD_REQUEST)

            valid_substance_ids = []
            if action != 'remove-all':
                valid_substance_ids = list(Substance.objects.filter(id__in=substances).values_list('id', flat=True))
            if regulation_id:
                add_substances = self.add_or_remove_substance_in_regulation(valid_substance_ids, regulation_id, action)
                add_or_remove_status = 'succeed' if add_substances else 'failed'
                add_info = f"regulation is {add_or_remove_status}"
            elif regulatory_framework_id:
                add_substances = self.add_or_remove_substance_in_framework(valid_substance_ids, regulatory_framework_id,
                                                                           action)
                add_or_remove_status = 'succeed' if add_substances else 'failed'
                add_info = f"regulatory framework is {add_or_remove_status}"
            else:
                add_substances = self.add_or_remove_substance_in_milestone(valid_substance_ids, milestone_id, action)
                add_or_remove_status = 'succeed' if add_substances else 'failed'
                add_info = f"milestone is {add_or_remove_status}"
            if action != 'remove-all':
                action_msg = action + (' in' if action == 'add' else ' from')
                response = {
                    'message': f"{len(valid_substance_ids)} substance(s) {action_msg} {add_info}"
                }
            else:
                response = {
                    "message": f"All the substances have been removed from {add_info}"
                }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def add_or_remove_substance_in_regulation(valid_substance_ids, regulation_id, action):
        try:
            regulation_queryset = Regulation.objects.get(id=regulation_id)
            if action == 'add':
                regulation_queryset.substances.add(*valid_substance_ids)
            elif action == 'remove-all':
                regulation_queryset.substances.clear()
            else:
                regulation_queryset.substances.remove(*valid_substance_ids)
            return True
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return False

    @staticmethod
    def add_or_remove_substance_in_framework(valid_substance_ids, framework_id, action):
        try:
            regulatory_framework_qs = RegulatoryFramework.objects.get(id=framework_id)
            if action == 'add':
                regulatory_framework_qs.substances.add(*valid_substance_ids)
            elif action == 'remove-all':
                regulatory_framework_qs.substances.clear()
            else:
                regulatory_framework_qs.substances.remove(*valid_substance_ids)
            return True
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return False

    @staticmethod
    def add_or_remove_substance_in_milestone(valid_substance_ids, milestone_id, action):
        try:
            milestone_qs = RegulationMilestone.objects.get(id=milestone_id)
            if action == 'add':
                milestone_qs.substances.add(*valid_substance_ids)
            elif action == 'remove-all':
                milestone_qs.substances.clear()
            else:
                milestone_qs.substances.remove(*valid_substance_ids)
            return True
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return False
