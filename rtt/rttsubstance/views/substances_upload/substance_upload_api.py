import logging
from datetime import datetime
from django.core.files.storage import default_storage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rttcore.permissions import IsSuperUserOrStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rttsubstance.models import SubstanceUploadLog, UserSubstanceAddLog, Substance
from re import sub
import openpyxl

from rttsubstance.tasks import substance_basic_details_upload_task, substances_uses_and_applications_upload_task, \
    substances_frameworks_or_regulations_upload_task, substance_related_products_upload_task, \
    substance_data_upload_task, substance_families_upload_task, user_substances_add_task,\
    admin_substance_data_upload_task, user_product_related_substances_upload_task, admin_substance_families_upload_task

logger = logging.getLogger(__name__)


class SubstanceUploadAPIView(APIView):
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
            enum=['Select one', 'substance-basic-details', 'substances-uses-applications',
                  'substances-in-frameworks-or-regulations', 'substance-related-products', 'substance-data',
                  'substance-families', 'admin-substance-data', 'admin-substance-families',
                  'substance-data-with-existing-data-decision']
        )],
        responses={400: 'Invalid data in uploaded file',
                   200: 'Success'},
    )
    def post(self, request, process_type, **kwargs):
        file_request = request.FILES['file']
        if str(file_request.content_type) != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return_msg = {
                'message': 'Invalid File Format. Only Excel will be accepted.',
            }
            return Response(return_msg, status=status.HTTP_400_BAD_REQUEST)
        log_process_type = self.get_process_type_name(process_type.lower())

        exist = SubstanceUploadLog.objects.filter(file_name=file_request.name).exists()
        if exist:
            return Response({"message": "File with same name already exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            substance_upload_log = SubstanceUploadLog.objects.create(
                file_name=file_request.name,
                process_type=log_process_type,
                status='in_queue',
                start_time=datetime.now(),
                end_time=datetime.now()
            )

        unique_file_name = str(datetime.now().microsecond) + '_' + file_request.name
        file_path = default_storage.save('substances_upload/' + unique_file_name, file_request)
        if process_type.lower() == 'substance-basic-details':
            substance_basic_details_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'substances-uses-applications':
            substances_uses_and_applications_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'substances-in-frameworks-or-regulations':
            substances_frameworks_or_regulations_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'substance-related-products':
            substance_related_products_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'substance-data':
            substance_data_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'substance-data-with-existing-data-decision':
            substance_data_upload_task.delay(file_path, file_request.name, substance_upload_log.id, existing_data_col=True)
        elif process_type.lower() == 'substance-families':
            substance_families_upload_task.delay(file_path, file_request.name, substance_upload_log.id)
        elif process_type.lower() == 'admin-substance-data':
            admin_substance_data_upload_task.delay(request.user.id, file_path, file_request.name,
                                                   substance_upload_log.id)
        elif process_type.lower() == 'admin-substance-families':
            is_file_format_correct = self.check_admin_substance_families_file_format(file_path, substance_upload_log.id)
            if not is_file_format_correct:
                return Response({"message": "The file format is wrong, please try again!"},
                                status=status.HTTP_400_BAD_REQUEST)
            family_id = request.data.get('family_id', None)
            error_message = self.check_substance_exist_and_is_family_true(family_id, substance_upload_log.id)
            if error_message:
                return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                admin_substance_families_upload_task.delay(request.user.id, file_path, file_request.name, family_id,
                                                           substance_upload_log.id)
        else:
            return Response({'message': 'Invalid process_type'}, status=status.HTTP_400_BAD_REQUEST)
        return_msg = f"File '{file_request.name}' is under process."
        return Response({'message': return_msg}, status=status.HTTP_200_OK)

    @staticmethod
    def get_process_type_name(process_type):
        if process_type.lower() == 'substance-basic-details':
            return 'substance_basic_details'
        elif process_type.lower() == 'substances-uses-applications':
            return 'substances_with_uses_and_applications'
        elif process_type.lower() == 'substances-in-frameworks-or-regulations':
            return 'substances_in_Regulatory_frameworks_or_Regulations'
        elif process_type.lower() == 'substance-related-products':
            return 'substance_related_products'
        elif process_type.lower() == 'substance-data':
            return 'substance_data'
        elif process_type.lower() == 'substance-families':
            return 'substance_families'
        elif process_type.lower() == 'admin-substance-data':
            return 'admin_substance_data'
        elif process_type.lower() == 'admin-substance-families':
            return 'admin_substance_families'
        elif process_type.lower() == 'substance-data-with-existing-data-decision':
            return 'substance_data_with_existing_data_decision'

    @staticmethod
    def check_admin_substance_families_file_format(file_path, substance_upload_log_id):
        """
        return True when file format is okay and False otherwise
        first column name: EC
        second column name: CAS
        Here column names are case-sensitive
        """
        try:
            substance_family_upload_log = SubstanceUploadLog.objects.get(id=substance_upload_log_id)
            file = default_storage.open(file_path)
            worksheet_data = openpyxl.load_workbook(file).worksheets[0]
            first_row = list(worksheet_data.iter_rows())[0]
            if first_row[0].value != "EC" or first_row[1].value != "CAS":
                substance_family_upload_log.traceback = "Missing/wrong column names"
                substance_family_upload_log.status = 'fail'
                substance_family_upload_log.save()
                return False
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return True

    @staticmethod
    def check_substance_exist_and_is_family_true(family_id, substance_upload_log_id):
        substance_family = Substance.objects.filter(id=family_id).first()
        error_message = None
        if not substance_family:
            error_message = "No substance found with this family Id"
        if substance_family and not substance_family.is_family:
            error_message = "Substance's is_family=false"

        if error_message:
            substance_family_upload_log = SubstanceUploadLog.objects.get(id=substance_upload_log_id)
            substance_family_upload_log.status = 'fail'
            substance_family_upload_log.traceback = error_message
            substance_family_upload_log.end_time = datetime.now()
            substance_family_upload_log.save()
        return error_message




class SubstanceAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, process_type, *args, **kwargs):
        try:
            file_request = request.FILES['file']
            if str(file_request.content_type) != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                return_msg = {
                    'message': 'Invalid File Format. Only Excel will be accepted.',
                }
                return Response(return_msg, status=status.HTTP_400_BAD_REQUEST)

            log_process_type = self.get_process_type_name(process_type.lower())
            user_substance_add_log = UserSubstanceAddLog.objects.create(
                file_name=file_request.name,
                process_type=log_process_type,
                user_id=request.user.id
            )

            unique_file_name = str(datetime.now().microsecond) + '_' + file_request.name
            file_path = default_storage.save('substances_upload/' + unique_file_name, file_request)
            if process_type.lower() == 'substances-add':
                uses_and_applications = request.data.get('uses_and_applications', None)
                if not uses_and_applications:
                    return Response({'message': 'uses_and_applications can not be empty'},
                                    status=status.HTTP_400_BAD_REQUEST)
                user_substance_add_log.object_type = 'uses_and_application'
                user_substance_add_log.save()
                user_substances_add_task.delay(request.user.id, request.user.organization_id, file_path,
                                               file_request.name,
                                               uses_and_applications, user_substance_add_log.id)

            elif process_type.lower() == 'product-related-substances-add':
                product_id = request.data.get('product_id', None)
                if not product_id:
                    return Response({'message': 'product can not be empty'},
                                    status=status.HTTP_400_BAD_REQUEST)
                user_substance_add_log.object_type = 'product'
                user_substance_add_log.save()
                user_product_related_substances_upload_task.delay(request.user.id, file_path, file_request.name,
                                                                  product_id, user_substance_add_log.id)

            return Response({'message': 'Import initiated, you will receive an email once it is completed'},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({'message': 'INTERNAL SERVER ERROR'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_process_type_name(process_type):
        if process_type.lower() == 'substances-add':
            return 'substance_add'
        elif process_type.lower() == 'product-related-substances-add':
            return 'product_related_substances_add'
