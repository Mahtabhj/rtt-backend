from rttregulation.documents import RegulatoryFrameworkDocument


class RegulationTaggedRegionService:

    @staticmethod
    def get_region_data(framework_id, serializer=True):
        result = []
        regulatory_framework_doc_qs: RegulatoryFrameworkDocument = RegulatoryFrameworkDocument().search().filter(
            'match', id=framework_id
        ).source(['regions'])
        regulatory_framework_doc_qs = regulatory_framework_doc_qs[0:regulatory_framework_doc_qs.count()]
        if not serializer:
            regions = []
            for framework in regulatory_framework_doc_qs:
                regions = framework.regions
            return regions
        for regulatory_framework in regulatory_framework_doc_qs:
            for region in regulatory_framework.regions:
                result.append({
                    'id': region.id,
                    'name': region.name
                })

        return result
