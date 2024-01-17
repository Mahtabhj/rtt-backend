from django.db.models import Q

from rttcore.services.id_search_service import IdSearchService
from rtttaskManagement.services.sequence_matcher_service import SequenceMatcherService
from rttregulation.models.models import RegulatoryFramework, Regulation
from rttproduct.models.models import Product
from rttsubstance.models import Substance
from rttnews.models.models import News


class EmailNotificationServices:

    def __init__(self):
        self.add_remove_id_found_service = AddRemoveIdFoundService()

    @staticmethod
    def name_field_process(old_name, new_name):
        has_diff, highlighted_name = SequenceMatcherService().get_highlighted_unified_diff_string(old_name, new_name)
        return has_diff, highlighted_name

    @staticmethod
    def description_field_process(old_description, new_description):
        has_diff, highlighted_description = SequenceMatcherService().get_highlighted_unified_diff_string(old_description,
                                                                                                         new_description)
        return has_diff, highlighted_description

    def regulatory_frameworks_field_process(self, old_frameworks, new_frameworks):
        results = []
        added_id_list = self.add_remove_id_found_service.get_added_id_list(old_frameworks, new_frameworks)
        removed_id_list = self.add_remove_id_found_service.get_removed_id_list(old_frameworks, new_frameworks)
        if len(added_id_list) == 0 and len(removed_id_list) == 0:
            return False, results
        framework_qs = RegulatoryFramework.objects.filter(Q(id__in=added_id_list) | Q(id__in=removed_id_list))
        for framework in framework_qs:
            results.append({
                'name': framework.name,
                'action': 'Added' if framework.id in added_id_list else 'Removed'
            })
        return True, results

    def regulations_field_process(self, old_regulations, new_regulations):
        results = []
        added_id_list = self.add_remove_id_found_service.get_added_id_list(old_regulations, new_regulations)
        removed_id_list = self.add_remove_id_found_service.get_removed_id_list(old_regulations, new_regulations)
        if len(added_id_list) == 0 and len(removed_id_list) == 0:
            return False, results
        regulation_qs = Regulation.objects.filter(Q(id__in=added_id_list) | Q(id__in=removed_id_list))
        for regulation in regulation_qs:
            results.append({
                'name': regulation.name,
                'action': 'Added' if regulation.id in added_id_list else 'Removed'
            })
        return True, results

    def products_field_process(self, old_products, new_products):
        results = []
        added_id_list = self.add_remove_id_found_service.get_added_id_list(old_products, new_products)
        removed_id_list = self.add_remove_id_found_service.get_removed_id_list(old_products, new_products)
        if len(added_id_list) == 0 and len(removed_id_list) == 0:
            return False, results
        product_qs = Product.objects.filter(Q(id__in=added_id_list) | Q(id__in=removed_id_list))
        for product in product_qs:
            results.append({
                'name': product.name,
                'action': 'Added' if product.id in added_id_list else 'Removed'
            })
        return True, results

    def substances_field_process(self, old_substances, new_substances):
        results = []
        added_id_list = self.add_remove_id_found_service.get_added_id_list(old_substances, new_substances)
        removed_id_list = self.add_remove_id_found_service.get_removed_id_list(old_substances, new_substances)
        if len(added_id_list) == 0 and len(removed_id_list) == 0:
            return False, results
        substances_qs = Substance.objects.filter(Q(id__in=added_id_list) | Q(id__in=removed_id_list))
        for substance in substances_qs:
            results.append({
                'name': substance.name,
                'action': 'Added' if substance.id in added_id_list else 'Removed'
            })
        return True, results

    def news_field_process(self, old_news, new_news):
        results = []
        added_id_list = self.add_remove_id_found_service.get_added_id_list(old_news, new_news)
        removed_id_list = self.add_remove_id_found_service.get_removed_id_list(old_news, new_news)
        if len(added_id_list) == 0 and len(removed_id_list) == 0:
            return False, results
        news_qs = News.objects.filter(Q(id__in=added_id_list) | Q(id__in=removed_id_list))
        for news in news_qs:
            results.append({
                'title': news.title,
                'action': 'Added' if news.id in added_id_list else 'Removed'
            })
        return True, results

    @staticmethod
    def doc_comment_add_process(old_doc_comment, new_doc_comment):
        has_diff, highlighted_doc_comment = SequenceMatcherService().get_highlighted_unified_diff_string(old_doc_comment,
                                                                                                         new_doc_comment)
        return has_diff, highlighted_doc_comment


class AddRemoveIdFoundService:

    def get_added_id_list(self, old_id_list: list, new_id_list: list):
        if len(old_id_list) == 0:
            return new_id_list
        added_id_list = self.get_newly_added_id_list(id_list=new_id_list, companion_id_list=old_id_list)
        return added_id_list

    def get_removed_id_list(self, old_id_list: list, new_id_list: list):
        if len(new_id_list) == 0:
            return old_id_list
        added_id_list = self.get_newly_added_id_list(id_list=old_id_list, companion_id_list=new_id_list)
        return added_id_list

    @staticmethod
    def get_newly_added_id_list(id_list: list, companion_id_list: list):
        results = []
        companion_id_list = sorted(companion_id_list)
        id_search_service = IdSearchService()
        for id in id_list:
            if not id_search_service.does_id_exit_in_sorted_list(companion_id_list, id):
                results.append(id)
        return results
