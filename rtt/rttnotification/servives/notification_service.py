from django.conf import settings
from django.db.models import Q
from elasticsearch_dsl import Q as esQ

import datetime
import pytz

from rttcore.services.dashboard_services import DashboardService
from rttcore.services.system_filter_service import SystemFilterService
from rttnews.documents import NewsRelevanceLogDocument
from rttregulation.documents import RegulationRatingLogDocument, RegulatoryFrameworkRatingLogDocument,\
    RegulatoryFrameworkDocument, RegulationDocument, MilestoneDocument
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttregulation.models.models import SubstanceRegulation, SubstanceRegulationMilestone, SubstanceRegulatoryFramework
from rttsubstance.documents import SubstanceDocument
from rttsubstance.models import SubstancePropertyDataPoint, Property, PropertyDataPoint, PrioritizationStrategy
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

utc = pytz.UTC
from rttproduct.services.category_validator_services import CategoryValidatorServices


class NotificationService:
    def __init__(self):
        self.base_url = settings.SITE_BASE_URL

    def get_news_notification_list(self, filters, organization_id):
        system_filter_service = SystemFilterService()

        news_queryset = system_filter_service.get_system_filtered_news_document_queryset(organization_id)\
            .filter('range', pub_date={'gte': filters['from_date'], 'lte': filters['to_date']})\
            .sort(
            {"regions.name": {
                "order": "asc",
                "nested": {
                    "path": "regions"
                }
            }
            })
        if filters.get('topics', None):
            news_queryset = news_queryset.filter(
                esQ('nested',
                    path='news_categories',
                    query=esQ('terms', news_categories__topic__id=filters['topics']))
            )
        if filters.get('regions', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='regions',
                query=esQ('terms', regions__id=filters['regions'])
            )
        if filters.get('product_categories', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='product_categories',
                query=esQ('terms', product_categories__id=filters['product_categories'])
            )
        if filters.get('material_categories', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='material_categories',
                query=esQ('terms', material_categories__id=filters['material_categories'])
            )
        if filters.get('related_frameworks', None):
            news_queryset = news_queryset.filter(
                'nested',
                path='regulatory_frameworks',
                query=esQ('terms', regulatory_frameworks__id=filters['related_frameworks'])
            )
        news_queryset = news_queryset[0:news_queryset.count()]
        # print(list(news_queryset))

        notification_list = []
        for news in news_queryset:
            regions = ', '.join(i['name'] for i in news.regions)
            product_categories = CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, news.product_categories, serialize=True)
            material_categories = CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, news.material_categories, serialize=True, distinct_item=False)
            product_categories, material_categories = self.get_product_and_material_categories_name(product_categories,
                                                                                                    material_categories)

            notification_list.append({
                "name": news.title,
                "pub_date": news.pub_date.strftime("%d %B, %Y"),
                "source_name": news.source.name if news.source else '',
                "regions": regions,
                "product_categories": product_categories,
                "material_categories": material_categories,
                "link": f'''{self.base_url}news/{news.id}''',
            })
        return notification_list

    def get_regulatory_updates_notification_list(self, filters, organization_id):
        system_filter_service = SystemFilterService()

        milestone_queryset = system_filter_service.get_system_filtered_milestone_document_queryset(organization_id) \
            .filter('range', from_date={'gte': filters['from_date'], 'lte': filters['to_date']})\
            .sort(
            {"regulatory_framework.regions.name": {
                "order": "asc",
                "nested": {
                    "path": "regulatory_framework.regions"
                }
            }
            },
            {"regulation.regulatory_framework.regions.name": {
                "order": "asc",
                "nested": {
                    "path": "regulation.regulatory_framework.regions"
                }
            }
            })

        if filters.get('topics', None):
            milestone_queryset = milestone_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.topics',
                    query=esQ('terms', regulatory_framework__topics__id=filters['topics'])) |
                esQ('nested',
                    path='regulation.topics',
                    query=esQ('terms', regulation__topics__id=filters['topics']))
            )
        if filters.get('regions', None):
            milestone_queryset = milestone_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.regions',
                    query=esQ('terms', regulatory_framework__regions__id=filters['regions'])) |
                esQ('terms', regulation__regulatory_framework__regions__id=filters['regions'])
            )
        if filters.get('product_categories', None):
            milestone_queryset = milestone_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.product_categories',
                    query=esQ('terms', regulatory_framework__product_categories__id=filters['product_categories'])) |
                esQ('nested',
                    path='regulation.product_categories',
                    query=esQ('terms', regulation__product_categories__id=filters['product_categories']))
            )
        if filters.get('material_categories', None):
            milestone_queryset = milestone_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.material_categories',
                    query=esQ('terms', regulatory_framework__material_categories__id=filters['material_categories'])) |
                esQ('nested',
                    path='regulation.material_categories',
                    query=esQ('terms', regulation__material_categories__id=filters['material_categories']))
            )
        if filters.get('related_frameworks', None):
            milestone_queryset = milestone_queryset.filter(
                esQ('terms', regulatory_framework__id=filters['related_frameworks']) |
                esQ('terms', regulation__regulatory_framework__id=filters['related_frameworks'])
            )

        milestone_queryset = milestone_queryset[0:milestone_queryset.count()]
        # print(list(milestone_queryset))

        notification_list = []
        for milestone in milestone_queryset:
            related_name = ''
            link = ''
            regions = ''
            product_categories = None
            material_categories = None

            if milestone.regulatory_framework:
                related_name = milestone.regulatory_framework.name
                regions = ', '.join(i['name'] for i in milestone.regulatory_framework.regions)
                link = f'''{self.base_url}regulations/regulatory-framework/{milestone.regulatory_framework.id}#milestone{milestone.id}'''
                product_categories = CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, milestone.regulatory_framework.product_categories, serialize=True)
                material_categories = CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, milestone.regulatory_framework.material_categories, serialize=True,
                    distinct_item=False)

            elif milestone.regulation:
                related_name = milestone.regulation.name
                if milestone.regulation.regulatory_framework:
                    regions = ', '.join(i['name'] for i in milestone.regulation.regulatory_framework.regions)
                link = f'''{self.base_url}regulations/regulation/{milestone.regulation.id}#milestone{milestone.id}'''
                product_categories = CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, milestone.regulation.product_categories, serialize=True)
                material_categories = CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, milestone.regulation.material_categories, serialize=True,
                    distinct_item=False)

            product_categories, material_categories = self.get_product_and_material_categories_name(
                product_categories, material_categories)
            if related_name:
                notification_list.append({
                    "name": milestone.name,
                    "related_name": related_name,
                    "regions": regions,
                    "date": milestone.from_date.strftime("%d %B, %Y"),
                    "product_categories": product_categories,
                    "material_categories":  material_categories,
                    "link": link,
                })
        notification_list.sort(key=lambda data: data['regions'], reverse=False)
        return notification_list

    def get_assessments_notification_list(self, filters, organization_id):
        rel_reg_ids = RelevantRegulationService().get_relevant_regulation_id_organization(organization_id)
        rel_fw_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(organization_id)
        regulation_rating_queryset = RegulationRatingLogDocument.search() \
            .filter('match', regulation__review_status='o') \
            .filter('terms', regulation__id=rel_reg_ids) \
            .filter('match', organization__id=organization_id) \
            .filter('range', created={'gte': filters['from_date'], 'lte': filters['to_date']}) \
            .sort('-created')
        framework_rating_queryset = RegulatoryFrameworkRatingLogDocument.search() \
            .filter('match', regulatory_framework__review_status='o') \
            .filter('terms', regulatory_framework__id=rel_fw_ids) \
            .filter('match', organization__id=organization_id) \
            .filter('range', created={'gte': filters['from_date'], 'lte': filters['to_date']}) \
            .sort('-created')
        news_rating_queryset = NewsRelevanceLogDocument.search() \
            .filter('match', news__status='s') \
            .filter('match', news__active=True) \
            .filter('match', organization__id=organization_id) \
            .filter('range', created={'gte': filters['from_date'], 'lte': filters['to_date']}) \
            .sort('-created')

        if filters.get('topics', None):
            regulation_rating_queryset = regulation_rating_queryset.filter(
                esQ('nested',
                    path='regulation.topics',
                    query=esQ('terms', regulation__topics__id=filters['topics']))
            )
            framework_rating_queryset = framework_rating_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.topics',
                    query=esQ('terms', regulatory_framework__topics__id=filters['topics']))
            )
            news_rating_queryset = news_rating_queryset.filter(
                esQ('nested',
                    path='news.news_categories',
                    query=esQ('terms', news__news_categories__topic__id=filters['topics']))
            )
        if filters.get('regions', None):
            regulation_rating_queryset = regulation_rating_queryset.filter(
                esQ('terms', regulation__regulatory_framework__regions__id=filters['regions'])
            )
            framework_rating_queryset = framework_rating_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.regions',
                    query=esQ('terms', regulatory_framework__regions__id=filters['regions']))
            )
            news_rating_queryset = news_rating_queryset.filter(
                esQ('nested',
                    path='news.regions',
                    query=esQ('terms', news__regions__id=filters['regions']))
            )
        if filters.get('product_categories', None):
            regulation_rating_queryset = regulation_rating_queryset.filter(
                esQ('nested',
                    path='regulation.product_categories',
                    query=esQ('terms', regulation__product_categories__id=filters['product_categories']))
            )
            framework_rating_queryset = framework_rating_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.product_categories',
                    query=esQ('terms', regulatory_framework__product_categories__id=filters['product_categories']))
            )
            news_rating_queryset = news_rating_queryset.filter(
                esQ('nested',
                    path='news.product_categories',
                    query=esQ('terms', news__product_categories__id=filters['product_categories']))
            )
        if filters.get('material_categories', None):
            regulation_rating_queryset = regulation_rating_queryset.filter(
                esQ('nested',
                    path='regulation.material_categories',
                    query=esQ('terms', regulation__material_categories__id=filters['material_categories']))
            )
            framework_rating_queryset = framework_rating_queryset.filter(
                esQ('nested',
                    path='regulatory_framework.material_categories',
                    query=esQ('terms', regulatory_framework__material_categories__id=filters['material_categories']))
            )
            news_rating_queryset = news_rating_queryset.filter(
                esQ('nested',
                    path='news.material_categories',
                    query=esQ('terms', news__material_categories__id=filters['material_categories']))
            )
        if filters.get('related_frameworks', None):
            regulation_rating_queryset = regulation_rating_queryset.filter(
                esQ('terms', regulation__regulatory_framework__id=filters['related_frameworks'])
            )
            framework_rating_queryset = framework_rating_queryset.filter(
                esQ('terms', regulatory_framework__id=filters['related_frameworks'])
            )
            news_rating_queryset = news_rating_queryset.filter(
                esQ('nested',
                    path='news.regulatory_frameworks',
                    query=esQ('terms', news__regulatory_frameworks__id=filters['related_frameworks']))
            )

        regulation_rating_queryset = regulation_rating_queryset[0:regulation_rating_queryset.count()]
        framework_rating_queryset = framework_rating_queryset[0:framework_rating_queryset.count()]
        news_rating_queryset = news_rating_queryset[0:news_rating_queryset.count()]

        regulation_rating_queryset = regulation_rating_queryset.to_queryset() \
            .distinct('created__date', 'regulation_id') \
            .order_by('-created__date', 'regulation_id', '-created') \
            .select_related('regulation')
        framework_rating_queryset = framework_rating_queryset.to_queryset() \
            .distinct('created__date', 'regulatory_framework_id') \
            .order_by('-created__date', 'regulatory_framework_id', '-created') \
            .select_related('regulatory_framework')
        news_rating_queryset = news_rating_queryset.to_queryset() \
            .distinct('created__date', 'news_id') \
            .order_by('-created__date', 'news_id', '-created') \
            .select_related('news')

        # print(list(regulation_rating_queryset), list(framework_rating_queryset), list(news_rating_queryset))

        notification_list = []
        for regulation_rating in regulation_rating_queryset:
            first_name = regulation_rating.user.first_name if regulation_rating.user.first_name else ''
            last_name = regulation_rating.user.last_name if regulation_rating.user.last_name else ''
            username = first_name + ' ' + last_name
            notification_list.append({
                "name": regulation_rating.regulation.name,
                "rating": regulation_rating.rating,
                "username": username,
                "date": regulation_rating.created.strftime("%d %B, %Y"),
                "sort_date": regulation_rating.created.strftime("%d/%m/%Y"),
                "link": f'''{self.base_url}regulations/regulation/{regulation_rating.regulation.id}''',
            })
        for framework_rating in framework_rating_queryset:
            first_name = framework_rating.user.first_name if framework_rating.user.first_name else ''
            last_name = framework_rating.user.last_name if framework_rating.user.last_name else ''
            username = first_name + ' ' + last_name
            notification_list.append({
                "name": framework_rating.regulatory_framework.name,
                "rating": framework_rating.rating,
                "username": username,
                "date": framework_rating.created.strftime("%d %B, %Y"),
                "sort_date": framework_rating.created.strftime("%d/%m/%Y"),
                "link": f'''{self.base_url}regulations/regulatory-framework/{framework_rating.regulatory_framework.id}''',
            })
        for news_rating in news_rating_queryset:
            first_name = news_rating.user.first_name if news_rating.user.first_name else ''
            last_name = news_rating.user.last_name if news_rating.user.last_name else ''
            username = first_name + ' ' + last_name
            notification_list.append({
                "name": news_rating.news.title,
                "rating": news_rating.relevancy,
                "username": username,
                "date": news_rating.created.strftime("%d %B, %Y"),
                "sort_date": news_rating.created.strftime("%d/%m/%Y"),
                "link": f'''{self.base_url}news/{news_rating.news.id}''',
            })

        notification_list.sort(key=lambda data: data['sort_date'], reverse=True)
        return notification_list

    def get_limit_notification_list(self, filters, organization_id):
        to_date = filters['to_date'][:11] + "23:59:59"
        limit_core_service = LimitCoreService()
        limit_qs = limit_core_service.get_regulation_substance_limit_queryset(
            organization_id, exclude_deleted=False).filter(
            esQ('range', modified={'gte': filters['from_date'], 'lte': to_date})
        )
        limit_qs = limit_qs[0:limit_qs.count()]

        notification_list = []
        for limit in limit_qs:

            if limit.regulatory_framework:
                is_regulation = False
                regulation_id = limit.regulatory_framework.id
                regulation_name = limit.regulatory_framework.name
                url = f'''{self.base_url}regulations/regulatory-framework/{limit.regulatory_framework.id}'''
            else:
                is_regulation = True
                regulation_id = limit.regulation.id
                regulation_name = limit.regulation.name
                url = f'''{self.base_url}regulations/regulation/{limit.regulation.id}'''

            if limit.status == 'deleted':
                change_status = '<p style="color:red"><b>Deleted</b></p>'
            else:
                if (limit.modified - limit.created).total_seconds() < 120:
                    change_status = '<p style="color:green"><b>Added</b></p>'
                else:
                    change_status = '<p style="color:blue"><b>Edited</b></p>'

            substance_qs = SubstanceDocument.search().filter(
                esQ('match', id=limit.substance.id)
            )
            substance = None
            for sub in substance_qs:
                substance = sub

            uses_and_applications_name = None
            if len(substance.uses_and_application_substances) > 0:
                uses_and_applications_name = '( '
                for idx, uses_and_applications in enumerate(substance.uses_and_application_substances):
                    if uses_and_applications.organization.id == organization_id:
                        if not idx == 0:
                            uses_and_applications_name += "; "
                        uses_and_applications_name += uses_and_applications.name
                uses_and_applications_name += ')'

            substance_limit = {
                'name': limit.substance.name,
                'ec_cas_no': "EC : " + (limit.substance.ec_no if limit.substance.ec_no else "") + "  " + "CAS:" +
                             (limit.substance.cas_no if limit.substance.cas_no else ""),
                'uses_and_applications': uses_and_applications_name,
            }
            additional_attributes = self.convert_additional_attribute_dictionary_to_string(
                limit.id, regulation_id, is_regulation)

            notification_list.append({
                "regulation": regulation_name,
                "substance": substance_limit,
                "scope": limit.scope,
                "limit_attributes": additional_attributes,
                "limit": str(limit.limit_value) + ' ' + str(limit.measurement_limit_unit),
                "action": change_status,
                "url": url,
            })
        return notification_list

    def get_substance_notification_list(self, filters, organization_id):

        milestone_ids, regulation_ids, framework_ids = self.get_related_milestone_regulation_framework_ids(
            organization_id)
        notification_framework_regulation_milestone = []

        # processing from date
        string_from_date = filters['from_date']
        year = int(string_from_date[:4])
        month = int(string_from_date[5:7])
        day = int(string_from_date[8:10])
        filters['from_date'] = datetime.datetime(year, month, day).replace(tzinfo=utc)
        # processing to date
        string_to_date = filters['to_date']
        year = int(string_to_date[:4])
        month = int(string_to_date[5:7])
        day = int(string_to_date[8:10])
        filters['to_date'] = datetime.datetime(year, month, day, 23, 59, 59).replace(tzinfo=utc)

        related_substances_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)

        substance_regulatory_framework_qs = SubstanceRegulatoryFramework.objects.filter(
            Q(substance__in=related_substances_ids) &
            Q(regulatory_framework__in=framework_ids) &
            Q(Q(modified__gte=filters['from_date']) & Q(modified__lte=filters['to_date']))
        )
        substance_regulation_qs = SubstanceRegulation.objects.filter(
            Q(substance__in=related_substances_ids) &
            Q(regulation__in=regulation_ids) &
            Q(Q(modified__gte=filters['from_date']) & Q(modified__lte=filters['to_date']))
        )
        substance_regulation_milestone_qs = SubstanceRegulationMilestone.objects.filter(
            Q(substance__in=related_substances_ids) &
            Q(regulation_milestone__in=milestone_ids) &
            Q(Q(modified__gte=filters['from_date']) & Q(modified__lte=filters['to_date']))
        )

        for substance_regulatory_framework in substance_regulatory_framework_qs:
            substance_qs = SubstanceDocument.search().filter(
                esQ('match', id=substance_regulatory_framework.substance_id)
            )
            substance = None
            for sub in substance_qs:
                substance = sub

            framework_qs = RegulatoryFrameworkDocument.search().filter(
                esQ('match', id=substance_regulatory_framework.regulatory_framework_id)
            )
            framework = None
            for fw in framework_qs:
                framework = fw

            url = f'''{self.base_url}regulations/regulatory-framework/{framework.id}'''
            notification_list_data = self.make_notification_list_for_substance(organization_id, 'Added', substance,
                                                                               "framework", framework.name, url)
            notification_framework_regulation_milestone.append(notification_list_data)

        for substance_regulation in substance_regulation_qs:
            substance_qs = SubstanceDocument.search().filter(
                esQ('match', id=substance_regulation.substance_id)
            )
            substance = None
            for sub in substance_qs:
                substance = sub

            regulation_qs = RegulationDocument.search().filter(
                esQ('match', id=substance_regulation.regulation_id)
            )
            regulation = None
            for reg in regulation_qs:
                regulation = reg

            url = f'''{self.base_url}regulations/regulation/{regulation.id}'''

            notification_list_data = self.make_notification_list_for_substance(organization_id, 'Added', substance,
                                                                               "regulation", regulation.name, url)
            notification_framework_regulation_milestone.append(notification_list_data)

        for substance_regulation_milestone in substance_regulation_milestone_qs:
            substance_qs = SubstanceDocument.search().filter(
                esQ('match', id=substance_regulation_milestone.substance_id)
            )
            substance = None
            for sub in substance_qs:
                substance = sub

            milestone_qs = MilestoneDocument.search().filter(
                esQ('match', id=substance_regulation_milestone.regulation_milestone_id)
            )
            milestone = None
            for mst in milestone_qs:
                milestone = mst

            if milestone.regulation:
                milestone_name = milestone.regulation.name + ' > ' + milestone.name
                url = f'''{self.base_url}regulations/regulation/{milestone.regulation.id}#milestone{milestone.id}'''
            else:
                milestone_name = milestone.regulatory_framework.name + ' > ' + milestone.name
                url = f'''{self.base_url}regulations/regulatory-framework/{milestone.regulatory_framework.id}#milestone{milestone.id}'''

            notification_list_data = self.make_notification_list_for_substance(organization_id, 'Added', substance,
                                                                               "milestone", milestone_name, url)
            notification_framework_regulation_milestone.append(notification_list_data)

        notification_property = self.make_notification_list_for_substance_property_data_point(organization_id,
                                                                                              filters)
        notification_list = {
            'notification_framework_regulation_milestone': notification_framework_regulation_milestone,
            'notification_property': notification_property,
            'has_table_one_data': True if len(notification_framework_regulation_milestone) > 0 else False,
            'has_table_two_data': True if len(notification_property) > 0 else False,
        }
        if len(notification_framework_regulation_milestone) == 0 and len(notification_property) == 0:
            notification_list = []

        return notification_list

    @staticmethod
    def get_related_milestone_regulation_framework_ids(organization_id):
        system_filter_service = SystemFilterService()
        milestone_ids = []
        regulation_ids = []
        framework_ids = []

        milestone_queryset = system_filter_service.get_system_filtered_milestone_document_queryset(organization_id)
        milestone_queryset = milestone_queryset[0:milestone_queryset.count()]
        for milestone in milestone_queryset:
            milestone_ids.append(milestone.id)

        regulation_queryset = system_filter_service.get_system_filtered_regulation_document_queryset(organization_id)
        regulation_queryset = regulation_queryset[0:regulation_queryset.count()]
        for regulation in regulation_queryset:
            regulation_ids.append(regulation.id)

        framework_queryset = system_filter_service.get_system_filtered_regulatory_framework_queryset(organization_id)
        framework_queryset = framework_queryset[0:framework_queryset.count()]
        for framework in framework_queryset:
            framework_ids.append(framework.id)

        return milestone_ids, regulation_ids, framework_ids

    def make_notification_list_for_substance(self, org_id, change_status, substance, relation_type, relation, url):
        uses_and_applications_name = None
        if len(substance.uses_and_application_substances) > 0:
            uses_and_applications_name = '( '
            for idx, uses_and_applications in enumerate(substance.uses_and_application_substances):
                if uses_and_applications.organization.id == org_id:
                    if not idx == 0:
                        uses_and_applications_name += "; "
                    uses_and_applications_name += uses_and_applications.name
            uses_and_applications_name += ')'

        substance_details = {
            'name': substance.name,
            'uses_and_applications': uses_and_applications_name,
        }

        notification_list_data = {
            'regulation': relation,
            'substance': substance_details,
            'ec_no': substance.ec_no if substance.ec_no else None,
            'cas_no': substance.cas_no if substance.cas_no else None,
            'action': change_status,
            'type': relation_type,
            'substance_url': f'''{self.base_url}substances/substance/{substance.id}''',
            'regulation_url': url
        }
        return notification_list_data

    def make_notification_list_for_substance_property_data_point(self, org_id, filters):
        results = []
        created_idx = {}
        substance_property_data_point_qs = SubstancePropertyDataPoint.objects.filter(
            Q(property_data_point__property__prioritization_strategy_properties__organization_id=org_id) &
            Q(Q(modified__gte=filters['from_date']) & Q(modified__lte=filters['to_date']))
        )
        for substance_property_data_point in substance_property_data_point_qs:
            substance_qs = SubstanceDocument.search().filter(
                esQ('match', id=substance_property_data_point.substance_id)
            )
            substance = None
            for sub in substance_qs:
                substance = sub

            uses_and_applications_name = None
            if len(substance.uses_and_application_substances) > 0:
                uses_and_applications_name = '( '
                for idx, uses_and_applications in enumerate(substance.uses_and_application_substances):
                    if uses_and_applications.organization.id == org_id:
                        if not idx == 0:
                            uses_and_applications_name += "; "
                        uses_and_applications_name += uses_and_applications.name
                uses_and_applications_name += ')'

            substance_details = {
                'name': substance.name,
                'uses_and_applications': uses_and_applications_name,
            }

            property_data_point_qs = PropertyDataPoint.objects.filter(id=substance_property_data_point.
                                                                      property_data_point_id).first()
            property_qs = Property.objects.filter(id=property_data_point_qs.property_id).first()

            if substance_property_data_point.status == 'deleted':
                change_status = '<p style="color:red"><b>Deleted</b></p>'
            else:
                if (substance_property_data_point.modified - substance_property_data_point.created).\
                        total_seconds() < 120:
                    change_status = '<p style="color:green"><b>Added</b></p>'
                else:
                    change_status = '<p style="color:blue"><b>Edited</b></p>'

            substance_property_obj = {
                'property': property_qs.name,
                'property_data_point': property_data_point_qs.name,
                'substance': substance_details,
                'cas_no': substance.cas_no if substance.cas_no else None,
                'value': substance_property_data_point.value,
                'action': change_status,
                'substance_url': f'''{self.base_url}substances/substance/{substance.id}''',
            }
            prioritization_strategy_qs = PrioritizationStrategy.objects.filter(organization_id=org_id,
                                                                               properties__id=property_qs.id)
            for prioritization_strategy in prioritization_strategy_qs:
                if not created_idx.get(prioritization_strategy.id, None):
                    created_idx[prioritization_strategy.id] = len(results) + 1
                    results.append({
                        "name": prioritization_strategy.name,
                        "substances": [substance_property_obj]
                    })
                else:
                    idx = created_idx.get(prioritization_strategy.id, None) - 1
                    results[idx]["substances"].append(substance_property_obj)

        return results

    @staticmethod
    def convert_additional_attribute_dictionary_to_string(limit_id, regulation_id, is_regulation):
        limit_attributes = AdditionalAttributesDataService().get_additional_attributes_data(
                    limit_id, regulation_id, is_regulation)
        result = ""
        for limit_attribute in limit_attributes:
            limit_attribute_info = f"Name: {limit_attribute['name']}, Value: {limit_attribute['value']}"
            result += limit_attribute_info
            result += '<br>'
        return result

    @staticmethod
    def get_product_and_material_categories_name(product_categories, material_categories):
        all_product_categories = ""
        for idx, prod_cat in enumerate(product_categories):
            if not idx == 0:
                all_product_categories += ", "
            all_product_categories += prod_cat['name']

        all_material_categories = ""
        for idx, mat_cat in enumerate(material_categories):
            if not idx == 0:
                all_material_categories += ", "
            all_material_categories += mat_cat['name']
            all_material_categories += "(" + mat_cat['industry']['name'] + ")"
        return all_product_categories, all_material_categories

