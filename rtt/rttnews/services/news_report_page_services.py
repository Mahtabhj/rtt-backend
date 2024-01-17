from elasticsearch_dsl import Q

from rttcore.services.dashboard_services import DashboardService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.rating_search_service import RatingSearchService


class NewsReportPageServices:
    RATING_LIST = [0, 1, 2, 3, 4, 5]

    def get_filtered_news_queryset(self, filters, organization_id):
        # apply DashboardService filter that call system filter as well
        news_doc_qs = DashboardService().get_filtered_news_queryset(filters, organization_id)
        # apply filter by rating
        news_doc_qs = self.rating_filtered_news_doc_qs(news_doc_qs, filters, organization_id)
        return news_doc_qs

    def rating_filtered_news_doc_qs(self, news_doc_qs, filters, organization_id):
        if filters.get('ratings', None):
            # if 0 in included then have to include Null value
            if 0 in filters['ratings']:
                news_doc_qs = news_doc_qs.filter(
                    Q(
                        # apply filter by rating eg: [0, 1, 2, 3, 4, 5]
                        Q('nested',
                          path='news_relevance',
                          query=Q('match', news_relevance__organization__id=organization_id) &
                            Q('terms', news_relevance__relevancy=filters['ratings'])) |
                        # apply filter by Null, which is considered as 0
                        ~Q('nested',
                           path='news_relevance',
                           query=Q('match', news_relevance__organization__id=organization_id) &
                           Q('terms', news_relevance__relevancy=self.RATING_LIST))
                    )
                )
            else:
                # if 0 is not included, then consider which are given
                news_doc_qs = news_doc_qs.filter(
                    # apply filter by rating eg: [1, 2, 3, 4, 5]
                    Q('nested',
                      path='news_relevance',
                      query=Q('terms', news_relevance__relevancy=filters['ratings']) &
                        Q('match', news_relevance__organization__id=organization_id))
                )
        return news_doc_qs

    @staticmethod
    def get_sorted_news_doc_qs(news_doc_qs, sort_order, organization_id):
        news_doc_qs = news_doc_qs.sort({
            "news_relevance.relevancy": {
                "order": sort_order,
                "nested_path": "news_relevance",
                "nested_filter": {
                    "term": {
                        "news_relevance.organization.id": organization_id
                    }
                }
            }
        }, {"pub_date": {"order": "desc"}})

        return news_doc_qs

    @staticmethod
    def get_news_object(news, organization_id):
        # fetch and store regions data
        region_list = []
        for region in news.regions:
            region_list.append({
                'id': region.id,
                'name': region.name
            })
        # this is response
        news_obj = {
            'id': news.id,
            'name': news.title,
            'regions': region_list,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id, news.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id, news.material_categories, serialize=True),
            'pub_date': news.pub_date,
            'impact_rating': RatingSearchService().get_news_rating_obj(organization_id, news.id)
        }
        return news_obj

    @staticmethod
    def get_rating_group_by_dict(organization_id):
        rating_group_by_dict = {
            "aggs": {
                "news_relevance": {
                    "nested": {
                        "path": "news_relevance"
                    },
                    "aggs": {
                        "news_relevance": {
                            "filter": {
                                "bool": {
                                    "filter": [
                                        {
                                            "term": {
                                                "news_relevance.organization.id": organization_id
                                            }
                                        }
                                    ]
                                }
                            },
                            "aggs": {
                                "results": {
                                    "terms": {
                                        "field": "news_relevance.relevancy",
                                        "size": 9999
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        return rating_group_by_dict
