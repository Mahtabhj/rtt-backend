from rttlimitManagement.models import LimitAdditionalAttributeValue


class AdditionalAttributesDataService:
    @staticmethod
    def get_additional_attributes_data(regulation_substance_limit_id, regulation_id, is_regulation=False):
        if is_regulation:
            additional_attributes_qs = LimitAdditionalAttributeValue.objects.filter(
                regulation_substance_limit_id=regulation_substance_limit_id,
                regulation_limit_attribute__regulation_id=regulation_id)
        else:
            additional_attributes_qs = LimitAdditionalAttributeValue.objects.filter(
                regulation_substance_limit_id=regulation_substance_limit_id,
                regulation_limit_attribute__regulatory_framework_id=regulation_id)
        result = []
        for additional_attribute in additional_attributes_qs:
            result.append({
                'id': additional_attribute.regulation_limit_attribute.id,
                'name': additional_attribute.regulation_limit_attribute.limit_attribute.name,
                'value': additional_attribute.value
            })
        return result
