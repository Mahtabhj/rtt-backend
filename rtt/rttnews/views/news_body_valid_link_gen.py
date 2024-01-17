from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
import time
from urllib.parse import urlparse, parse_qs

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rttnews.models.models import News
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)

class NewsBodyValidLinkGenAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'link': openapi.Schema(type=openapi.TYPE_STRING, description='send URL link',
                                      example="https://{bucket-name}.s3.amazonaws.com/{file-path}?AWSAccessKeyId={unique-key}&Signature={unique-key}&Expires={Unix-time}"),
        }
    ))
    def post(self, request, news_id, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1399
        """
        try:
            # if url link is not sent in the payload return
            if not request.data.get("link", None):
                return Response({"message": "URL link must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            link = request.data["link"]
            parsed_url = urlparse(link)
            query = parse_qs(parsed_url.query)

            # if resource is not exists return
            if not S3Boto3Storage().exists(parsed_url.path):
                return Response({"message": "invalid link or resource not found"}, status=status.HTTP_400_BAD_REQUEST)

            # if url link has validity don't generate new url link
            expire_time = int(query['Expires'][0])
            if not self.has_expired(expire_time):
                return Response(link, status=status.HTTP_200_OK)

            # generate new url link
            new_link = S3Boto3Storage().url(parsed_url.path)
            # replace the new link in the news body
            self.update_news_body(news_id, link, new_link)
            return Response(new_link, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def has_expired(expire_time: int):
        expire_limit = int(time.time()) + int(86400)
        if expire_time - expire_limit > 0:
            return False
        return True

    @staticmethod
    def update_news_body(news_id, old_link:str, new_link:str):
        # fetch the news by news_id and replace the url link with new url link and save the news body in the DB
        news_obj = News.objects.get(id=news_id)
        news_body = news_obj.body
        news_body = news_body.replace(old_link, new_link)
        news_obj.body = news_body
        news_obj.save()
