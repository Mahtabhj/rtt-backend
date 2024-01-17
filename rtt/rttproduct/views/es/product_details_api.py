from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttproduct.documents import ProductDocument


class ProductDetailsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, product_id):
        organization_id = request.user.organization_id
        product_queryset = ProductDocument.search().filter(
            'match', organization__id=organization_id).filter('match', id=product_id)
        last_mentioned = ''
        try:
            last_mentioned = list(product_queryset)[0].last_mentioned
        except IndexError:
            pass
        product_queryset = product_queryset.to_queryset().first()
        if not product_queryset:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        product_details = {
            'id': product_queryset.id,
            'name': product_queryset.name,
            'description': product_queryset.description,
            'image': product_queryset.image.url if product_queryset.image else None,
            'last_mentioned': last_mentioned,
            'regulation_count': 0,
            'news_count': 0,
            'product_categories': [],
            'material_categories': [],
            'related_products': [],
            'substance_use_and_apps': [],
        }

        news_count = 0
        regulation_count = 0
        for product_category in product_queryset.product_categories.all():
            news_count = news_count + product_category.product_category_news.count()
            regulation_count = regulation_count + product_category.regulation_product_categories.count()
            product_details['product_categories'].append({'id': product_category.id, 'name': product_category.name})

        product_details['news_count'] = news_count
        product_details['regulation_count'] = regulation_count

        for material_category in product_queryset.material_categories.all():
            product_details['material_categories'].append({
                'id': material_category.id,
                'name': material_category.name,
                'short_name': material_category.short_name,
                'industry': {
                    'id': material_category.industry.id,
                    'name': material_category.industry.name
                }
            })

        for sub_use_and_app in product_queryset.substance_use_and_apps.all():
            if sub_use_and_app.organization.id == organization_id:
                product_details['substance_use_and_apps'].append({
                    'id': sub_use_and_app.id,
                    'name': sub_use_and_app.name,
                })

        return Response(product_details, status=status.HTTP_200_OK)
