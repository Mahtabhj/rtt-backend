from rttorganization.services.organization_services import OrganizationService


class CategoryValidatorServices:
    @staticmethod
    def get_relevant_product_categories(organization_id, product_categories, serialize=False):
        relevant_product_categories = []
        organization_product_category_ids = OrganizationService().get_organization_product_category_ids(
            organization_id)
        if not serialize:
            return [k for k in product_categories if k['id'] in organization_product_category_ids]
        for product_cat in product_categories:
            if product_cat.id in organization_product_category_ids:
                relevant_product_categories.append({'id': product_cat.id, 'name': product_cat.name})
        return relevant_product_categories

    @staticmethod
    def get_relevant_material_categories(organization_id, material_categories, serialize=False, distinct_item=True):
        relevant_material_categories = []
        visited_material_categories = {}
        organization_material_category_ids = OrganizationService().get_organization_material_category_ids(
            organization_id)
        if not serialize:
            return [k for k in material_categories if k['id'] in organization_material_category_ids]
        for material_cat in material_categories:
            if material_cat.id in organization_material_category_ids:
                if distinct_item and material_cat.name.lower() not in visited_material_categories:
                    relevant_material_categories.append({
                        'id': material_cat.id,
                        'name': material_cat.name,
                        'short_name': material_cat.short_name
                    })
                    visited_material_categories[material_cat.name.lower()] = True
                elif not distinct_item:
                    relevant_material_categories.append({
                        'id': material_cat.id,
                        'name': material_cat.name,
                        'short_name': material_cat.short_name,
                        'industry': {
                            'id': material_cat.industry.id,
                            'name': material_cat.industry.name
                        },
                    })
        return relevant_material_categories
