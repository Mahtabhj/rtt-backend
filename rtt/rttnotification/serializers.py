from rest_framework import serializers

from rttnotification.models import NotificationAlert
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService


class NotificationAlertSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        user = self.context['request'].user
        data['user'] = user.id
        return super().to_internal_value(data)
    
    class Meta:
        model = NotificationAlert
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        organization_id = self.context['request'].user.organization_id
        if instance.regulatory_frameworks:
            rel_fw_ids = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(organization_id)
            temp_frameworks = data['regulatory_frameworks']
            data['regulatory_frameworks'] = []
            for framework in temp_frameworks:
                if IdSearchService().does_id_exit_in_sorted_list(rel_fw_ids, framework):
                    data['regulatory_frameworks'].append(framework)
        return data
