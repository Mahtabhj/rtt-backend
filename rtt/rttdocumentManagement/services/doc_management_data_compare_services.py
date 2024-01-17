class DocManagementDataCompareServices:
    @staticmethod
    def get_updated_doc_management_data_dict(serializer: dict):
        updated_data = {
            'name': serializer.get('name', ''),
            'description': serializer.get('description', ''),
            'regulatory_frameworks': [],
            'regulations': [],
            'products': [],
            'substances': [],
            'news': [],
        }
        # regulatory_frameworks
        if serializer.get('regulatory_frameworks', None):
            for fw in serializer['regulatory_frameworks']:
                updated_data['regulatory_frameworks'].append(fw['id'])
        # regulations
        if serializer.get('regulations', None):
            for reg in serializer['regulations']:
                updated_data['regulations'].append(reg['id'])
        # products
        if serializer.get('products', None):
            for product in serializer['products']:
                updated_data['products'].append(product['id'])
        # substances
        if serializer.get('substances', None):
            for sub in serializer['substances']:
                updated_data['substances'].append(sub['id'])
        #
        if serializer.get('news', None):
            for news in serializer['news']:
                updated_data['news'].append(news['id'])

        return updated_data

    @staticmethod
    def get_old_doc_management_data_dict(instance):
        old_data = {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'regulatory_frameworks': [fw.id for fw in instance.regulatory_frameworks.all()],
            'regulations': [reg.id for reg in instance.regulations.all()],
            'products': [product.id for product in instance.products.all()],
            'substances': [sub.id for sub in instance.substances.all()],
            'news': [news.id for news in instance.news.all()],
        }
        return old_data