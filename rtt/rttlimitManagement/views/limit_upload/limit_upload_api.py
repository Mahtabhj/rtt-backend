from datetime import datetime
from django.core.files.storage import default_storage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rttcore.permissions import IsSuperUserOrStaff
from rest_framework.views import APIView
from rest_framework.response import Response

from rttlimitManagement.models import LimitUploadLog
from rttlimitManagement.tasks import regulation_substance_limit_upload_task, exemption_upload_task, \
    limit_additional_attribute_value_upload_task, limit_with_additional_attribute_value_upload_task


class LimitUploadAPIView(APIView):
    permission_classes = [IsSuperUserOrStaff]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description='Upload excel file',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="Document"
        ), openapi.Parameter(
            name="process_type",
            in_=openapi.IN_PATH,
            type=openapi.TYPE_STRING,
            required=True,
            enum=['Select one', 'regulation_substance_limit', 'exemption', 'limit_additional_attribute_value',
                  'limit_with_additional_attribute_value']
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request, process_type, **kwargs):
        file_request = request.FILES.get('file', None)
        if not file_request:
            return Response({"message": "A excel file obj must be sent in file parameter"},
                            status=status.HTTP_400_BAD_REQUEST)
        if str(file_request.content_type) != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return_msg = {
                'message': 'Invalid File Format. Only Excel will be accepted.',
            }
            return Response(return_msg, status=status.HTTP_400_BAD_REQUEST)
        exist = LimitUploadLog.objects.filter(file_name=file_request.name).exists()
        if exist:
            return Response({"message": "File with same name already exist"}, status=status.HTTP_400_BAD_REQUEST)
        log_process_type = self.get_process_type_name(process_type.lower())
        limit_upload_log = LimitUploadLog.objects.create(
            file_name=file_request.name,
            process_type=log_process_type,
            status='in_queue',
            user_id=request.user.id,
            end_time=datetime.now()
        )
        unique_file_name = str(datetime.now().microsecond) + '_' + file_request.name
        file_path = default_storage.save('limit_upload/' + unique_file_name, file_request)
        if process_type.lower() == 'regulation_substance_limit':
            regulation_substance_limit_upload_task.delay(file_path, file_request.name, limit_upload_log.id)
        elif process_type.lower() == 'exemption':
            exemption_upload_task.delay(file_path, file_request.name, request.user.email, limit_upload_log.id)
        elif process_type.lower() == 'limit_additional_attribute_value':
            limit_additional_attribute_value_upload_task.delay(file_path, file_request.name, limit_upload_log.id)
        elif process_type.lower() == 'limit_with_additional_attribute_value':
            limit_with_additional_attribute_value_upload_task.delay(request.user.id, file_path, file_request.name,
                                                                    limit_upload_log.id)
        else:
            return Response({'message': 'Invalid process_type'}, status=status.HTTP_400_BAD_REQUEST)
        return_msg = f"File '{file_request.name}' is under process."
        return Response({'message': return_msg}, status=status.HTTP_200_OK)

    @staticmethod
    def get_process_type_name(process_type):
        if process_type in ['regulation_substance_limit', 'exemption', 'limit_additional_attribute_value',
                            'limit_with_additional_attribute_value']:
            return process_type
        return ''
