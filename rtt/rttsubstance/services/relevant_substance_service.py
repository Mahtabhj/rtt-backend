from elasticsearch_dsl import Q
from django.conf import settings
from django.core.cache import cache as django_cache

from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttsubstance.models import SubstanceUsesAndApplication


class RelevantSubstanceService:

    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_organization_relevant_substance_ids(self, organization_id):
        """
            params:
            organization_id : int

            Return a list of relevant_substance_ids of an organization in ascending order
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('organization_substances_{}'.format(organization_id))
        if cache_data:
            return cache_data

        organization_substances_ids = []
        organization_substances_qs = SubstanceCoreService().get_filtered_substance_queryset(organization_id).sort('id')
        organization_substances_qs = organization_substances_qs[0:organization_substances_qs.count()]
        for substance in organization_substances_qs:
            organization_substances_ids.append(substance.id)

        '''
        set data into django cache
        '''
        django_cache.set('organization_substances_{}'.format(organization_id),
                         organization_substances_ids,
                         self.django_cache_timeout)

        return organization_substances_ids

    @staticmethod
    def get_organization_relevant_substance_data(organization_id, data_name, data_id, search_keyword=None,
                                                 serializer=False, only_my_org=True, product_detail_page=False):
        """
        This function will return organization_relevant_substance_data queryset when serializer is False or
        organization_relevant_substance_data dict when serializer is True. Here data_name is either 'news', 'framework',
        'regulation', or 'product', or 'milestone'. And data_id is news_id, or framework_id, or regulation_id, or
        product_id or milestone_id.
        :param organization_id: User's organization.
        :param data_name: 'news', 'framework', 'regulation', 'product', 'milestone'
        :param data_id: news_id, framework_id, regulation_id, product_id, milestone_id
        :param search_keyword: key_word will be searched in substance_name, substance_ec_no and substance_cas_no field
        :param serializer: Boolean value. Default value is False
        :param only_my_org: Boolean value. Default value is True
        :param product_detail_page: Boolean value. when use in the product details page, then substances list will
        include related substances and substances which are tagged via use_and_app to that product
        :return: substance queryset or substance_dict
        """
        if only_my_org:
            organization_substances_qs = SubstanceCoreService().get_filtered_substance_queryset(organization_id)
        else:
            organization_substances_qs = SubstanceCoreService().get_filtered_substance_queryset(
                organization_id, only_my_org=only_my_org)

        if search_keyword:
            if product_detail_page:
                # keyword search in substances name, ec_no and cas_no and use&app_name
                organization_substances_qs = organization_substances_qs.query(
                    Q('match', name=search_keyword) |
                    Q('match_phrase', ec_no=search_keyword) |
                    Q('match_phrase', cas_no=search_keyword) |
                    Q('match', ec_no=search_keyword) |
                    Q('match', cas_no=search_keyword) |
                    Q('nested',
                      path='uses_and_application_substances',
                      query=Q('match', uses_and_application_substances__name=search_keyword) &
                            Q('match', uses_and_application_substances__organization__id=organization_id))
                ).sort("_score")
            else:
                # keyword search in substances name, ec_no and cas_no
                organization_substances_qs = organization_substances_qs.query(
                    Q('match', name=search_keyword) |
                    Q('match_phrase', ec_no=search_keyword) |
                    Q('match_phrase', cas_no=search_keyword) |
                    Q('match', ec_no=search_keyword) |
                    Q('match', cas_no=search_keyword)
                ).sort("_score")
        # substances tagged in news
        if data_name == 'news':
            organization_substances_qs = organization_substances_qs.filter(
                Q('nested',
                  path='substances_news',
                  query=Q('match', substances_news__id=data_id))
            )
        # substances tagged in framework
        if data_name == 'framework':
            organization_substances_qs = organization_substances_qs.filter(
                Q('nested',
                  path='substances_regulatory_framework',
                  query=Q('match', substances_regulatory_framework__id=data_id))
            )
        # substances tagged in regulation
        if data_name == 'regulation':
            organization_substances_qs = organization_substances_qs.filter(
                Q('nested',
                  path='substances_regulation',
                  query=Q('match', substances_regulation__id=data_id))
            )
        # substances tagged in product
        if data_name == 'product':
            if product_detail_page:
                product_tagged_use_and_app_list = list(SubstanceUsesAndApplication.objects.filter(
                    product_substance_use_and_apps=data_id).values_list('id', flat=True))
                organization_substances_qs = organization_substances_qs.filter(
                    Q('nested',
                      path='substances_product',
                      query=Q('match', substances_product__id=data_id)) |
                    Q('nested',
                      path='uses_and_application_substances',
                      query=Q('terms', uses_and_application_substances__id=product_tagged_use_and_app_list) &
                            Q('match', uses_and_application_substances__organization__id=organization_id))
                )
            else:
                organization_substances_qs = organization_substances_qs.filter(
                    Q('nested',
                      path='substances_product',
                      query=Q('match', substances_product__id=data_id))
                )
        # substances tagged in milestone
        if data_name == 'milestone':
            organization_substances_qs = organization_substances_qs.filter(
                Q('nested',
                  path='substances_regulation_milestone',
                  query=Q('match', substances_regulation_milestone__id=data_id))
            )

        if not serializer:
            return organization_substances_qs
        organization_substances_qs = organization_substances_qs[0:organization_substances_qs.count()]

        organization_substances_data = []
        for substance in organization_substances_qs:
            organization_substances_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no
            }
            organization_substances_data.append(organization_substances_obj)
        return organization_substances_data

    @staticmethod
    def get_substance_and_organization(substance_doc_queryset):
        """
        This function take substance_doc_queryset and return list of substance_obj and org  when that substance belongs
        to. Sample:
                    result = [
                        {
                            'id': 1,
                            'name': substance_name,
                            'ec_no': substance_ec_no,
                            'cas_no': substance_cas_no,
                            'organization': [
                                {
                                    'id': organization_id,
                                    'name': organization_name
                                }
                            ]
                        }
                    ]
        :param queryset substance_doc_queryset: Required. SubstanceDocument

        """
        result = []
        for substance in substance_doc_queryset:
            substance_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no,
                'organization': []
            }
            visited_organization = {}
            for uses_and_application in substance.uses_and_application_substances:
                if uses_and_application.organization and \
                        str(uses_and_application.organization.id) not in visited_organization:
                    substance_obj['organization'].append({
                        'id': uses_and_application.organization.id,
                        'name': uses_and_application.organization.name
                    })
                    visited_organization[str(uses_and_application.organization.id)] = True
            result.append(substance_obj)
        return result
