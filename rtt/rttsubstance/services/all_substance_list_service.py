from rttsubstance.documents import SubstanceDocument
from elasticsearch_dsl import Q


class AllSubstanceListService:
    @staticmethod
    def get_all_substance_list(search_keyword, limit=100, skip=0):
        result = []
        substance_search_qs: SubstanceDocument = SubstanceDocument.search().query(
            # keyword search in substances name, ec_no and cas_no
            Q('match', name=search_keyword) |
            Q('match_phrase', ec_no=search_keyword) | Q('match_phrase', cas_no=search_keyword) |
            Q('match', ec_no=search_keyword) | Q('match', cas_no=search_keyword)) \
            .sort("_score")
        substance_search_qs = substance_search_qs[skip:limit+skip]
        for substance in substance_search_qs:
            organization_substances_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no
            }
            result.append(organization_substances_obj)
        return result
