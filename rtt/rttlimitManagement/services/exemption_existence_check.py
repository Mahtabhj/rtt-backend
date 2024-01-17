from elasticsearch_dsl import Q

from rttlimitManagement.documents import ExemptionDocument
from rttsubstance.models import Substance


class ExemptionExistenceCheck:
    @staticmethod
    def has_exemption_data(regulation_id, is_regulation, substance_id):
        """
        This function take regulation_id, is_regulation and substance_id then check is there any exemption
        for these regulation_id and substance_id. Return true if there is any exemption and false otherwise
        :param int regulation_id: required, id of a regulation/framework,
        :param bool is_regulation: required, is_regulation if regulation_id is an id of regulation and false if
        regulation_id is an id of regulatory_framework,
        :param int substance_id: required, id of a substance.
        """
        substance_id_list = [substance_id]
        is_family = Substance.objects.filter(is_family=True, id=substance_id).exists()
        if is_family:
            child_substance_id_list = list(Substance.objects.filter(substance_family__family=substance_id).values_list(
                'id', flat=True))
            substance_id_list.extend(child_substance_id_list)
        if is_regulation:
            has_exemption: ExemptionDocument = ExemptionDocument.search().filter('match', status='active').filter(
                Q('terms', substance__id=substance_id_list) &
                Q('match', regulation__id=regulation_id)
            )
        else:
            has_exemption: ExemptionDocument = ExemptionDocument.search().filter('match', status='active').filter(
                Q('terms', substance__id=substance_id_list) &
                Q('match', regulatory_framework__id=regulation_id)
            )
        return has_exemption.count() > 0
