import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db.models import Q
from rest_framework import status

from rttnews.models.models import News, Source, NewsCategory, AutomaticFileImportNewsSource
from rttnews.serializers.serializers import NewsDocumentSaveSerializer
from rttnews.services.news_service import NewsService
from rttregulation.models.models import Region
from rttsubstance.models import Substance


class NewsApiService:
    """
    This service get news and related data from chemical api and save in RTT database
    """

    def __init__(self):
        self.chemical_base_url = settings.CHEMICAL_BASE_URL
        self.chemical_client_id = settings.CHEMICAL_CLIENT_ID
        self.chemical_client_name = settings.CHEMICAL_CLIENT_NAME
        # self.token = 'Bearer ' + self.get_token().json()
        # self.headers = {'Authorization': self.token, 'accept': 'application/json'}
        self.token = ''
        self.headers = ''

    def get_token(self):
        url = self.chemical_base_url + 'auth/token'
        body = {'clientName': self.chemical_client_name, 'clientId': self.chemical_client_id}
        return requests.post(url, headers={'clientName': 'application/json'}, json=body, timeout=60)

    def get_news(self, from_date):
        url = self.chemical_base_url + 'news?pageOffset=0&pageSize=50000&date=' + from_date
        print('news_url: ', url)
        return requests.get(url, headers=self.headers)

    def get_source(self, source_id):
        url = self.chemical_base_url + 'source/' + source_id
        return requests.get(url, headers=self.headers)

    def get_category(self, category_id):
        url = self.chemical_base_url + 'category/' + category_id
        return requests.get(url, headers=self.headers)

    def get_region(self, region_id):
        url = self.chemical_base_url + 'zone/' + region_id
        return requests.get(url, headers=self.headers)

    def set_token_header(self, token_response):
        self.token = 'Bearer ' + token_response.json()
        self.headers = {'Authorization': self.token, 'accept': 'application/json'}

    def process_news(self, from_date):
        try:
            response = {}
            token_response = self.get_token()
            if token_response.status_code == 200:
                self.set_token_header(token_response)
                news_response = self.get_news(from_date)
                if news_response.status_code == 200:
                    news_list = news_response.json()
                    list_size = len(news_list)
                    print('News size: ', list_size)
                    # print('News list: ', news_list)
                    self.process_news_data(news_list)
                    response = {
                        'msg': 'successful!',
                        'status': news_response.status_code,
                        'list_size':  list_size
                    }
                else:
                    print('News error: ', news_response.status_code)
                    response = {
                        'msg': 'News error!',
                        'status': news_response.status_code
                    }
            else:
                print('Token error: ', token_response.status_code)
                response = {
                    'msg': 'Token error!',
                    'status': token_response.status_code
                }
            print('Chemical news save done')
            return response
        except Exception:
            print('An exception occurred in news process')
            raise

    def save_news_categories(self, categories):
        category_list = []
        for category in categories:
            category_response = self.get_category(category['id'])
            if category_response.status_code == 200:
                category_obj = self.save_category(category_response.json())
                category_list.append(category_obj)
        return category_list

    def save_news_regions(self, regions):
        region_list = []
        for region in regions:
            region_response = self.get_region(region['id'])
            if region_response.status_code == 200:
                region_obj = self.save_region(region_response.json())
                region_list.append(region_obj)
        return region_list

    def save_news_substances(self, substances):
        substance_list = []
        for substance in substances:
            substance_obj = self.save_substance(substance)
            substance_list.append(substance_obj)
        return substance_list

    def process_news_data(self, news_list):
        for news in news_list:
            source_response = self.get_source(news['sourceId'])
            if source_response.status_code == 200:
                news['source'] = self.save_source(source_response.json())
            category_list = self.save_news_categories(news['categories'])
            region_list = self.save_news_regions(news['zones'])
            substance_list = self.save_news_substances(news['substances'])
            news['body'] = self.clean_substance_tag(news['body'])
            self.save_news(news, category_list, region_list, substance_list)

    def save_news(self, news, category_list, region_list, substance_list):
        obj = News.objects.filter(Q(chemical_id=news['id']) | Q(title=news['title'])).first()
        if not obj:
            try:
                obj = News(
                    active=True,
                    body=news['body'],
                    chemical_id=news['id'],
                    # cover_image=news['newsImage'],
                    pub_date=news['publicationDate'],
                    source=news.get('source', None),
                    title=news['title'],
                )
                obj.save()
                obj.news_categories.add(*category_list)
                obj.regions.add(*region_list)
                obj.save()
                self.precess_news_automatic_document_import(obj)
            except Exception:
                print('Chemical news save error for news_id: ', news['id'])
                raise

        if obj.status in ['n', 's']:
            obj.substances.add(*substance_list)
            obj.save()
        return obj

    @staticmethod
    def save_source(source):
        obj = Source.objects.filter(Q(chemical_id=source['id']) | Q(name=source['name'])).first()
        if not obj:
            try:
                obj = Source(
                    chemical_id=source['id'],
                    description=source['description'],
                    link=source['link'],
                    name=source['name'],
                )
                obj.save()
            except Exception:
                print('Chemical source save error for source_id: ', source['id'])
                raise
        return obj

    @staticmethod
    def save_category(category):
        obj = NewsCategory.objects.filter(Q(chemical_id=category['id']) | Q(name=category['name'])).first()
        if not obj:
            try:
                obj = NewsCategory(
                    active=True,
                    chemical_id=category['id'],
                    description=category['description'],
                    name=category['name']
                )
                obj.save()
            except Exception:
                print('Chemical NewsCategory save error for category_id: ', category['id'])
                raise
        return obj

    @staticmethod
    def save_region(region):
        obj = Region.objects.filter(Q(chemical_id=region['id']) | Q(name=region['title'])).first()
        if not obj:
            try:
                obj = Region(
                    chemical_id=region['id'],
                    iso_name=region['isoName'],
                    latitude=region['latitude'],
                    longitude=region['longitude'],
                    name=region['title'],
                )
                obj.save()
            except Exception:
                print('Chemical Region save error for region_id: ', region['id'])
                raise
        return obj

    @staticmethod
    def save_substance(substance):
        obj = Substance.objects.filter(chemycal_id__iexact=substance['id']).first()
        if not obj:
            try:
                obj = Substance(
                    chemycal_id=substance['id'],
                    name=substance['name'],
                    ec_no=substance['ecNumber'],
                    cas_no=substance['casNumber'],
                )
                obj.save()
            except Exception:
                print('Chemical substance save error for substance_id: ', substance['id'])
                raise
        return obj

    @staticmethod
    def clean_substance_tag(news_body):
        """
        Clean tags to substances from news body. Remove the a tag from the
        substances but will keep the substanceId in the span as metadata.
        sample output: <span substance_id="26ef38d9">silver</span>
        """
        soup = BeautifulSoup(news_body, 'html.parser')
        for a in soup.find_all('a', {'class': 'blog-tags'}):
            href_split = a['href'].split('/')
            if len(href_split) == 6:
                substance_id = href_split[4]
                if substance_id != '':
                    substance_span = soup.new_tag('span', substance_id=substance_id)
                    substance_span.string = a.text
                    a.replace_with(substance_span)
        news_body = str(soup)
        return news_body

    @staticmethod
    def precess_news_automatic_document_import(news_obj):
        if news_obj.source:
            default_setting = AutomaticFileImportNewsSource.objects.filter(news_source=news_obj.source.id).first()
            if default_setting:
                news_service = NewsService()
                news_doc_data = news_service.get_news_body_documents(news_obj.body)
                new_body = news_obj.body
                valid_document_idx = []
                has_edit = False
                for news_doc in news_doc_data:
                    news_doc['type'] = default_setting.document_type_id
                    news_doc['description'] = news_doc['title']
                    serializer = NewsDocumentSaveSerializer(data=news_doc)
                    if serializer.is_valid():
                        document = serializer.save(serializer.data.get('link'))
                        valid_document_idx.append(document.id)
                        new_body = new_body.replace(news_doc['link'], document.attachment.url, 1)
                        has_edit = True
                if has_edit:
                    news_obj.documents.add(*valid_document_idx)
                    news_obj.body = new_body
                    news_obj.save()
