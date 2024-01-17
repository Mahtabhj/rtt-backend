from rest_framework import pagination
from rest_framework.response import Response

from rttnews.models.models import News


class NewsPagination(pagination.PageNumberPagination):
    page_size = 999999
    page_size_query_param = 'pageSize'
    max_page_size = 100000
    page_query_param = 'pageNumber'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'review_count': News.objects.filter(review_yellow=True, review_green=False).count(),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
