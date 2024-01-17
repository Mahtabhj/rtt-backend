from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

from rttcore.permissions import IsSuperUserOrStaff
from rttsubstance.tasks import upload_substances_add_relation_task

logger = logging.getLogger(__name__)


class UploadSubstanceAddRelationAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description='Upload excel file',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Document"
        ),
            openapi.Parameter(
                name="regulation_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="input regulation_id"
            ),
            openapi.Parameter(
                name="regulatory_framework_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="input regulatory_framework_id"
            ),
            openapi.Parameter(
                name="milestone_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="input milestone_id"
            )
        ],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-876 --> add via excel
        """
        try:
            file_request = request.FILES['file']
            if str(file_request.content_type) != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                return_msg = {
                    'message': 'Invalid File Format. Only Excel will be accepted.',
                }
                return Response(return_msg, status=status.HTTP_400_BAD_REQUEST)
            regulation_id = request.data.get('regulation_id', None)
            regulatory_framework_id = request.data.get('regulatory_framework_id', None)
            milestone_id = request.data.get('milestone_id', None)
            param_count = 0
            process_type = None
            object_id = None
            if regulation_id:
                param_count += 1
                process_type = 'regulation'
                object_id = regulation_id
            if regulatory_framework_id:
                param_count += 1
                process_type = 'regulatory_framework'
                object_id = regulatory_framework_id
            if milestone_id:
                param_count += 1
                process_type = 'milestone'
                object_id = milestone_id
            if param_count != 1:
                return Response({"message": "regulation_id OR regulatory_framework_id OR milestone_id must be sent"},
                                status=status.HTTP_400_BAD_REQUEST)
            unique_file_name = str(datetime.now().microsecond) + '_' + file_request.name
            file_path = default_storage.save('substance_upload/' + unique_file_name, file_request)
            upload_substances_add_relation_task.delay(file_path, file_request.name, process_type, object_id,
                                                      request.user.email)
            return_msg = "Import initiated, you will receive an email once it is completed."
            return Response({'message': return_msg}, status=status.HTTP_200_OK)
        except Exception as ex:
            logging.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
