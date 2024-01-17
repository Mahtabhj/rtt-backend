from elasticsearch_dsl import Q
from rttdocumentManagement.documents import DocumentManagementDocument

class DocumentManagementCoreService:
    def __init__(self, organization_id):
        self.organization_id = organization_id

    def get_filtered_doc_management_doc_qs(self, filters, search_keyword):
        # filter doc_management which is relevant for organization
        doc_management_doc_qs: DocumentManagementDocument = DocumentManagementDocument.search().filter(
            'match', uploaded_by__organization__id=self.organization_id
        )
        # filter by search_keyword
        if search_keyword:
            doc_management_doc_qs = self.get_keyword_searched_doc_queryset(doc_management_doc_qs, search_keyword)

        if not filters:
            return doc_management_doc_qs

        # filter by regulatory_frameworks
        if filters.get('regulatory_frameworks', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('nested',
                  path='regulatory_frameworks',
                  query=Q('terms', regulatory_frameworks__id=filters['regulatory_frameworks']))
            )

        # filter by regulations
        if filters.get('regulations', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('nested',
                  path='regulations',
                  query=Q('terms', regulations__id=filters['regulations']))
            )

        # filter by products
        if filters.get('products', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('nested',
                  path='products',
                  query=Q('terms', products__id=filters['products']))
            )

        # filter by substances
        if filters.get('substances', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('nested',
                  path='substances',
                  query=Q('terms', substances__id=filters['substances']))
            )

        # filter by news
        if filters.get('news', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('nested',
                  path='news',
                  query=Q('terms', news__id=filters['news']))
            )

        # filter by uploaded_by
        if filters.get('uploaded_by', None):
            doc_management_doc_qs = doc_management_doc_qs.filter(
                Q('terms', uploaded_by__id=filters['uploaded_by'])
            )

        # filter by date range(from_date-to_date)
        if filters.get('from_date', None) and filters.get('to_date', None):
            from_date = filters['from_date']
            to_date = filters['to_date']
            doc_management_doc_qs = doc_management_doc_qs.filter(
                'range', modified={'gte': from_date, 'lte': to_date}
            )

        return doc_management_doc_qs

    @staticmethod
    def get_keyword_searched_doc_queryset(doc_management_doc_qs, search_keyword):
        doc_management_doc_qs = doc_management_doc_qs.query(
            # any keyword, which will be searched in Document name
            Q('match', name=search_keyword) |
            # any keyword, which will be searched in document description
            Q('match', description=search_keyword) |
            # any keyword, which will be searched in regulatory_frameworks name
            Q('nested',
              path='regulatory_frameworks',
              query=Q('match', regulatory_frameworks__name=search_keyword)) |
            # any keyword, which will be searched in regulations name
            Q('nested',
              path='regulations',
              query=Q('match', regulations__name=search_keyword)) |
            # any keyword, which will be searched in product name
            Q('nested',
              path='products',
              query=Q('match', products__name=search_keyword)) |
            # any keyword, which will be searched in substance name, ec_no, cas_no
            Q('nested',
              path='substances',
              query=Q('match', substances__name=search_keyword) |
                    Q('match_phrase', substances__ec_no=search_keyword) |
                    Q('match', substances__ec_no=search_keyword) |
                    Q('match_phrase', substances__cas_no=search_keyword) |
                    Q('match', substances__cas_no=search_keyword)) |
            # any keyword, which will be searched in news title
            Q('nested',
              path='news',
              query=Q('match', news__title=search_keyword)) |
            # any keyword, which will be searched in first_name of the assignee
            Q('match', uploaded_by__first_name=search_keyword) |
            # any keyword. which will be searched in last_name of the assignee
            Q('match', uploaded_by__last_name=search_keyword)
        ).sort("_score")

        return doc_management_doc_qs
