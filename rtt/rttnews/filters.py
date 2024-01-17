import django_filters

from rttdocument.filters import NumberInFilter
from rttnews.models.models import News


class NewsFilter(django_filters.FilterSet):
    regions = NumberInFilter(field_name='regions', lookup_expr='in')
    source = NumberInFilter(field_name='source', lookup_expr='in')
    news_categories = NumberInFilter(field_name='news_categories', lookup_expr='in')
    product_categories = NumberInFilter(field_name='product_categories', lookup_expr='in')

    class Meta:
        model = News
        fields = ('regions', 'source', 'news_categories', 'product_categories', 'status', 'active',  'review_green',
                  'review_yellow')
