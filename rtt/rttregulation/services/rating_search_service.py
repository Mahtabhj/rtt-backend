from rttnews.models.models import NewsRelevance
from rttregulation.models.models import RegulatoryFrameworkRating, RegulationRating


class RatingSearchService:

    def get_news_rating(self, organization_id, news_id):
        news_rating = 0
        news_rating_queryset = self.get_news_rating_queryset(organization_id, news_id)
        if news_rating_queryset:
            news_rating = news_rating_queryset.relevancy
        return news_rating

    def get_regulation_rating(self, organization_id, regulation_id):
        regulation_rating = 0
        regulation_rating_queryset = self.get_regulation_rating_queryset(organization_id, regulation_id)
        if regulation_rating_queryset:
            regulation_rating = regulation_rating_queryset.rating
        return regulation_rating

    def get_news_rating_obj(self, organization_id, news_id, news_relevance_list=None):
        news_rating_queryset = None
        if news_relevance_list:
            filtered_data = list(filter(lambda x: x.organization.id == organization_id, news_relevance_list))
            if filtered_data:
                news_rating_queryset = filtered_data[0]
        else:
            news_rating_queryset = self.get_news_rating_queryset(organization_id, news_id)
        if news_rating_queryset is None:
            return None
        news_rating_obj = {}
        if news_rating_queryset:
            news_rating_obj = {
                'id': news_rating_queryset.id,
                'rating': news_rating_queryset.relevancy,
                'comment': news_rating_queryset.comment,
                'created': news_rating_queryset.created
            }
        return news_rating_obj

    def get_regulation_rating_obj(self, organization_id, regulation_id, regulation_rating_list=None):
        regulation_rating_queryset = None
        if regulation_rating_list:
            filtered_data = list(filter(lambda x: x.organization.id == organization_id, regulation_rating_list))
            if filtered_data:
                regulation_rating_queryset = filtered_data[0]
        else:
            regulation_rating_queryset = self.get_regulation_rating_queryset(organization_id, regulation_id)
        if regulation_rating_queryset is None:
            return None

        regulation_rating_obj = {}
        if regulation_rating_queryset:
            regulation_rating_obj = {
                'id': regulation_rating_queryset.id,
                'rating': regulation_rating_queryset.rating,
                'comment': regulation_rating_queryset.comment,
                'created': regulation_rating_queryset.created
            }
        return regulation_rating_obj

    def get_framework_rating_obj(self, organization_id, framework_id, framework_rating_list=None):
        framework_rating_queryset = None
        if framework_rating_list:
            filtered_data = list(filter(lambda x: x.organization.id == organization_id, framework_rating_list))
            if filtered_data:
                framework_rating_queryset = filtered_data[0]
        else:
            framework_rating_queryset = self.get_framework_rating_queryset(organization_id, framework_id)
        if framework_rating_queryset is None:
            return None

        framework_rating_obj = {}
        if framework_rating_queryset:
            framework_rating_obj = {
                'id': framework_rating_queryset.id,
                'rating': framework_rating_queryset.rating,
                'comment': framework_rating_queryset.comment,
                'created': framework_rating_queryset.created
            }
        return framework_rating_obj

    @staticmethod
    def get_news_rating_queryset(organization_id, news_id):
        news_rating_queryset = NewsRelevance.objects\
            .filter(organization_id=organization_id, news_id=news_id) \
            .order_by('id').last()
        return news_rating_queryset

    @staticmethod
    def get_framework_rating_queryset(organization_id, framework_id):
        framework_rating_queryset = RegulatoryFrameworkRating.objects\
            .filter(organization_id=organization_id, regulatory_framework_id=framework_id) \
            .order_by('id').last()
        return framework_rating_queryset

    @staticmethod
    def get_regulation_rating_queryset(organization_id, regulation_id):
        regulation_rating_queryset = RegulationRating.objects\
            .filter(organization_id=organization_id, regulation__id=regulation_id) \
            .order_by('id').last()
        return regulation_rating_queryset
