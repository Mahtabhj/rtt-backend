from rttdocument.documents import DocumentModelDocument
from rttnews.documents import NewsDocument
from elasticsearch_dsl import Q

from rttorganization.services.organization_services import OrganizationService
from rttregulation.documents import RegulationDocument, RegulatoryFrameworkDocument, MilestoneDocument
from rttregulation.models.core_models import Topic
from django.core.cache import cache as django_cache
from django.conf import settings


class SystemFilterService:
    def __init__(self):
        # cache timeout in seconds
        self.django_cache_timeout = settings.DJANGO_CACHE_TIMEOUT

    def get_system_filtered_news_document_queryset(self, organization_id):
        """
        params:
        organization_id : user organization_id (int)

        Return a filtered news_document_queryset:NewsDocument
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('news_document_queryset_organization_{}'.format(organization_id))
        # print('news_cache: ', cache_data)
        if cache_data:
            return cache_data

        news_document_queryset: NewsDocument = NewsDocument.search()
        organization_service = OrganizationService()
        organization_product_category_ids = organization_service.get_organization_product_category_ids(organization_id)
        organization_material_category_ids = organization_service.get_organization_material_category_ids(
            organization_id)
        organization_topics = list(
            Topic.objects.filter(industry_topics__organization_industries__id=organization_id).values_list('id',
                                                                                                           flat=True))

        # system filtered regulatory_framework
        framework_doc_qs = self.get_system_filtered_regulatory_framework_queryset(organization_id).source(['id'])
        framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
        framework_ids = []
        for framework in framework_doc_qs:
            framework_ids.append(framework.id)
        # system filtered regulation
        regulation_doc_qs = self.get_system_filtered_regulation_document_queryset(organization_id).source(['id'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        regulation_ids = []
        for regulation in regulation_doc_qs:
            regulation_ids.append(regulation.id)
        '''
        system filters 
        docs: https://chemycal.atlassian.net/browse/RTT-445
        '''
        news_document_queryset = news_document_queryset.filter(
            Q('bool',
              must=[Q('match', active=True), Q('match', status='s')],
              should=[
                  # news material_categories
                  Q('nested',
                    path='material_categories',
                    query=Q('terms', material_categories__id=organization_material_category_ids)),
                  # news product_categories
                  Q('nested',
                    path='product_categories',
                    query=Q('terms', product_categories__id=organization_product_category_ids)),

                  # related regulatory_frameworks
                  Q('nested',
                    path='regulatory_frameworks',
                    query=Q('terms', regulatory_frameworks__id=framework_ids)),

                  # related regulation
                  Q('nested',
                    path='regulations',
                    query=Q('terms', regulations__id=regulation_ids)),

                  # news_categories topics
                  # https://chemycal.atlassian.net/browse/RTT-445?focusedCommentId=10770
                  Q('bool',
                    must_not=[Q('nested',
                                path='product_categories',
                                query=Q('exists',
                                        field='product_categories')),
                              Q('nested',
                                path='material_categories',
                                query=Q('exists',
                                        field='material_categories')),
                              Q('nested',
                                path='regulations',
                                query=Q('exists',
                                        field='regulations')),
                              Q('nested',
                                path='regulatory_frameworks',
                                query=Q('exists',
                                        field='regulatory_frameworks')),
                              ],
                    must=[Q('nested',
                            path='news_categories',
                            query=Q('terms', news_categories__topic__id=organization_topics))]
                    )
              ],
              minimum_should_match=1
              )
        )

        '''
        set data into django cache
        '''
        django_cache.set('news_document_queryset_organization_{}'.format(organization_id), news_document_queryset,
                         self.django_cache_timeout)
        return news_document_queryset

    def get_system_filtered_regulation_document_queryset(self, organization_id, is_muted=False, apply_mute_filter=True):
        """
        params:
        organization_id : user organization_id (int)
        apply_mute_filter: indicates that whether, have to apply is_muted or not
        is_muted: if true have to send those are is_muted=True and is_muted=False otherwise

        Return a filtered regulation_document_queryset: RegulationDocument
        """

        '''
        check in django_cache
        '''
        # cache_data = django_cache.get('regulation_document_queryset_organization_{}'.format(organization_id))
        # print('regulation_cache: ', cache_data)
        # if cache_data:
        #     return cache_data

        regulation_document_queryset: RegulationDocument = RegulationDocument.search()
        '''
        doc: Mute/Unmute a framework/regulation --> https://chemycal.atlassian.net/browse/RTT-964
        '''
        if apply_mute_filter:
            if is_muted:
                regulation_document_queryset = regulation_document_queryset.filter(
                    Q('nested',
                      path='regulation_mute_regulation',
                      query=Q('match', regulation_mute_regulation__organization__id=organization_id) &
                           Q('match', regulation_mute_regulation__is_muted=is_muted))
                )
            else:
                regulation_document_queryset = regulation_document_queryset.filter(
                    Q('nested',
                      path='regulation_mute_regulation',
                      query=(Q('match', regulation_mute_regulation__organization__id=organization_id) &
                             Q('match', regulation_mute_regulation__is_muted=is_muted))) |
                    ~Q('nested',
                       path='regulation_mute_regulation',
                       query=(Q('match', regulation_mute_regulation__organization__id=organization_id) &
                              Q('exists', field='regulation_mute_regulation')))
                )
        organization_service = OrganizationService()
        organization_product_category_ids = organization_service.get_organization_product_category_ids(organization_id)
        organization_material_category_ids = organization_service.get_organization_material_category_ids(
            organization_id)

        '''
        system filters
        docs: https://chemycal.atlassian.net/browse/RTT-446
        '''
        regulation_document_queryset = regulation_document_queryset.filter(
            Q('bool',
              must=[Q('match', review_status='o')],
              should=[
                  # regulation material_categories
                  Q('nested',
                    path='material_categories',
                    query=Q('terms', material_categories__id=organization_material_category_ids)),

                  # regulation product_categories
                  Q('nested',
                    path='product_categories',
                    query=Q('terms', product_categories__id=organization_product_category_ids))],
              minimum_should_match=1
              )
        )

        '''
        set data into django cache
        '''
        # django_cache.set('regulation_document_queryset_organization_{}'.format(organization_id),
        #                  regulation_document_queryset, self.django_cache_timeout)
        return regulation_document_queryset

    def get_system_filtered_regulatory_framework_queryset(self, organization_id, is_muted=False,
                                                          apply_mute_filter=True, apply_regulation_mute=False):
        """
        params:
        organization_id : user organization_id (int)
        apply_mute_filter: indicates that whether, have to apply is_muted or not
        is_muted: if true have to send those are is_muted=True and is_muted=False otherwise

        Return a filtered regulatory_framework_document_queryset:RegulatoryFrameworkDocument
        """

        '''
        check in django_cache
        '''
        # cache_data = django_cache.get(
        #     'regulatory_framework_document_queryset_organization_{}'.format(organization_id))
        # print('regulatory_framework_cache', cache_data)
        # if cache_data:
        #     return cache_data

        regulatory_framework_document_queryset: RegulatoryFrameworkDocument = RegulatoryFrameworkDocument.search()
        '''
        doc: Mute/Unmute a framework/regulation --> https://chemycal.atlassian.net/browse/RTT-964
        '''
        if apply_mute_filter:
            regulation_id_list = []
            if apply_regulation_mute:
                regulation_document_queryset = self.get_system_filtered_regulation_document_queryset(
                    organization_id, is_muted).source(['id'])
                regulation_document_queryset = regulation_document_queryset[0:regulation_document_queryset.count()]
                for regulation in regulation_document_queryset:
                    regulation_id_list.append(regulation.id)
            if is_muted:
                if apply_regulation_mute:
                    regulatory_framework_document_queryset = regulatory_framework_document_queryset.filter(
                        Q('nested',
                          path='regulation_mute_framework',
                          query=Q('match', regulation_mute_framework__organization__id=organization_id) &
                               Q('match', regulation_mute_framework__is_muted=is_muted)) |
                        Q('nested',
                          path='regulation_regulatory_framework',
                          query=Q('terms', regulation_regulatory_framework__id=regulation_id_list))
                    )
                else:
                    regulatory_framework_document_queryset = regulatory_framework_document_queryset.filter(
                        Q('nested',
                          path='regulation_mute_framework',
                          query=Q('match', regulation_mute_framework__organization__id=organization_id) &
                               Q('match', regulation_mute_framework__is_muted=is_muted))
                    )
            else:
                if apply_regulation_mute:
                    regulatory_framework_document_queryset = regulatory_framework_document_queryset.filter(
                        Q('nested',
                          path='regulation_mute_framework',
                          query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                                 Q('match', regulation_mute_framework__is_muted=is_muted))) |
                        ~Q('nested',
                           path='regulation_mute_framework',
                           query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                                  Q('exists', field='regulation_mute_framework'))) |
                        Q('nested',
                          path='regulation_regulatory_framework',
                          query=Q('terms', regulation_regulatory_framework__id=regulation_id_list))
                    )
                else:
                    regulatory_framework_document_queryset = regulatory_framework_document_queryset.filter(
                        Q('nested',
                          path='regulation_mute_framework',
                          query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                                 Q('match', regulation_mute_framework__is_muted=is_muted))) |
                        ~Q('nested',
                           path='regulation_mute_framework',
                           query=(Q('match', regulation_mute_framework__organization__id=organization_id) &
                                  Q('exists', field='regulation_mute_framework')))
                    )
        organization_service = OrganizationService()
        organization_product_category_ids = organization_service.get_organization_product_category_ids(organization_id)
        organization_material_category_ids = organization_service.get_organization_material_category_ids(
            organization_id)

        '''
        system filters
        https://chemycal.atlassian.net/browse/RTT-446
        '''
        regulatory_framework_document_queryset = regulatory_framework_document_queryset.filter(
            Q('bool',
              must=[Q('match', review_status='o')],
              should=[
                  # regulatory_framework material_categories
                  Q('nested',
                    path='material_categories',
                    query=Q('terms', material_categories__id=organization_material_category_ids)),
                  # regulatory_framework product_categories
                  Q('nested',
                    path='product_categories',
                    query=Q('terms', product_categories__id=organization_product_category_ids)),

                  # related regulation
                  Q('bool',
                    must=[Q('nested',
                            path='regulation_regulatory_framework',
                            query=Q('match', regulation_regulatory_framework__review_status='o'))],
                    should=[
                        # related regulations material_categories
                        Q('nested',
                          path='regulation_regulatory_framework.material_categories',
                          query=Q('terms',
                                  regulation_regulatory_framework__material_categories__id=organization_material_category_ids)),

                        # related regulations product_categories
                        Q('nested',
                          path='regulation_regulatory_framework.product_categories',
                          query=Q('terms',
                                  regulation_regulatory_framework__product_categories__id=organization_product_category_ids))
                    ],
                    minimum_should_match=1
                    )
              ],
              minimum_should_match=1
              )
        )

        '''
        set data into django cache
        '''
        # django_cache.set('regulatory_framework_document_queryset_organization_{}'.format(organization_id),
        #                  regulatory_framework_document_queryset, self.django_cache_timeout)
        return regulatory_framework_document_queryset

    def get_system_filtered_milestone_document_queryset(self, organization_id, is_muted=False, apply_mute_filter=True):
        """
        params:
        organization_id : user organization_id (int)

        Return a filtered milestone_document_queryset: MilestoneDocument
        """

        '''
        check in django_cache
        '''
        # cache_data = django_cache.get('milestone_document_queryset_organization_{}'.format(organization_id))
        # print('milestone_cache: ', cache_data)
        # if cache_data:
        #     return cache_data

        milestone_document_queryset: MilestoneDocument = MilestoneDocument.search()
        """
        mute un-mute logic doc: https://chemycal.atlassian.net/browse/RTT-1135
        """
        if apply_mute_filter:
            if is_muted:
                milestone_document_queryset = milestone_document_queryset.filter(
                    Q('nested',
                      path='milestone_mute_milestone',
                      query=Q('match', milestone_mute_milestone__organization__id=organization_id) &
                           Q('match', milestone_mute_milestone__is_muted=is_muted))
                )
            else:
                milestone_document_queryset = milestone_document_queryset.filter(
                    Q('nested',
                      path='milestone_mute_milestone',
                      query=(Q('match', milestone_mute_milestone__organization__id=organization_id) &
                             Q('match', milestone_mute_milestone__is_muted=is_muted))) |
                    ~Q('nested',
                       path='milestone_mute_milestone',
                       query=(Q('match', milestone_mute_milestone__organization__id=organization_id) &
                              Q('exists', field='milestone_mute_milestone')))
                )

        # system filtered regulatory_framework
        framework_doc_qs = self.get_system_filtered_regulatory_framework_queryset(organization_id).source(['id'])
        framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
        framework_ids = []
        for framework in framework_doc_qs:
            framework_ids.append(framework.id)
        # system filtered regulation
        regulation_doc_qs = self.get_system_filtered_regulation_document_queryset(organization_id).source(['id'])
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
        regulation_ids = []
        for regulation in regulation_doc_qs:
            regulation_ids.append(regulation.id)
        '''
        system filters
        docs: https://chemycal.atlassian.net/browse/RTT-446
        '''
        milestone_document_queryset = milestone_document_queryset.filter(
            Q('bool',
              should=[
                  # regulation
                  Q('terms', regulation__id=regulation_ids),
                  # regulatory_framework
                  Q('terms', regulatory_framework__id=framework_ids),
              ],
              minimum_should_match=1
              )
        )

        '''
        set data into django cache
        '''
        # django_cache.set('milestone_document_queryset_organization_{}'.format(organization_id),
        #                  milestone_document_queryset, self.django_cache_timeout)
        return milestone_document_queryset

    def get_system_filtered_document_model_document_queryset(self, organization_id):
        """
        params:
        organization_id : user organization_id (int)

        Return a filtered document_model_document_queryset: DocumentModelDocument
        """

        '''
        check in django_cache
        '''
        cache_data = django_cache.get('document_model_document_queryset_organization_{}'.format(organization_id))
        # print('document_model_cache: ', cache_data)
        if cache_data:
            return cache_data

        document_model_document_queryset: DocumentModelDocument = DocumentModelDocument.search()
        organization_service = OrganizationService()
        organization_product_category_ids = organization_service.get_organization_product_category_ids(organization_id)
        organization_material_category_ids = organization_service.get_organization_material_category_ids(
            organization_id)

        '''
        system filters
        docs: https://chemycal.atlassian.net/browse/RTT-446
        docs: https://chemycal.atlassian.net/browse/RTT-445
        '''
        document_model_document_queryset = document_model_document_queryset.filter(
            Q('bool',
              should=[
                  # regulation
                  Q('bool',
                    must=[Q('nested',
                            path='regulation_documents',
                            query=Q('match', regulation_documents__review_status='o'))],
                    should=[
                        # regulation material_categories
                        Q('nested',
                          path='regulation_documents.material_categories',
                          query=Q('terms',
                                  regulation_documents__material_categories__id=organization_material_category_ids)),

                        # regulation product_categories
                        Q('nested',
                          path='regulation_documents.product_categories',
                          query=Q('terms',
                                  regulation_documents__product_categories__id=organization_product_category_ids)),
                    ],
                    minimum_should_match=1
                    ),

                  # regulatory_framework
                  Q('bool',
                    must=[Q('nested',
                            path='framework_documents',
                            query=Q('match', framework_documents__review_status='o'))],
                    should=[
                        # regulatory_framework material_categories
                        Q('nested',
                          path='framework_documents.material_categories',
                          query=Q('terms',
                                  framework_documents__material_categories__id=organization_material_category_ids)),

                        # regulatory_framework product_categories
                        Q('nested',
                          path='framework_documents.product_categories',
                          query=Q('terms',
                                  framework_documents__product_categories__id=organization_product_category_ids)),
                    ],
                    minimum_should_match=1
                    ),

                  # news
                  Q('bool',
                    must=[Q('nested',
                            path='news_documents',
                            query=Q('match', news_documents__active=True)),
                          Q('nested',
                            path='news_documents',
                            query=Q('match', news_documents__status='s'))
                          ],
                    should=[
                        # news material_categories
                        Q('nested',
                          path='news_documents.material_categories',
                          query=Q('terms', news_documents__material_categories__id=organization_material_category_ids)),

                        # news product_categories
                        Q('nested',
                          path='news_documents.product_categories',
                          query=Q('terms', news_documents__product_categories__id=organization_product_category_ids))
                    ],
                    minimum_should_match=1
                    )
              ],
              minimum_should_match=1
              )
        )

        '''
        set data into django cache
        '''
        django_cache.set('document_model_document_queryset_organization_{}'.format(organization_id),
                         document_model_document_queryset, self.django_cache_timeout)
        return document_model_document_queryset
