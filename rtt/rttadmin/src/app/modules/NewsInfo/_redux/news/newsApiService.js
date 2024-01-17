import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const NEWS_URL = BASE_URL + "news/";
const REGULATION_URL = BASE_URL + "regulation/";
const REGULATORY_FRAMEWORK_URL = BASE_URL + "regulatory-framework/";
const PRODUCT_CATEGORY_URL = BASE_URL + "product-categories/";
const MATERIAL_CATEGORY_URL = BASE_URL + "material-categories/";
const ORGANIZATION_URL = BASE_URL + "organizations/";
const DOCUMENT_URL = BASE_URL + "documents/";
const DOCUMENT_TYPE_URL = BASE_URL + "document-type/";
const INDUSTRIES_URL = BASE_URL + "industries/";
const RELEVANCE_URL = BASE_URL + "news-relevance/";
const DOCUMENTS_URL = BASE_URL + "documents/";
const NEWS_SOURCE = BASE_URL + "news-source/";
const NEWS_CATEGORY = BASE_URL + "news-category/";
const NEWS_RELEVANT = BASE_URL + "news/get_relevant_organizations/";
const NEWS_FROM_API = NEWS_URL + "get_news_from_api/"
const REGION_URL = BASE_URL + "region/";

// CREATE =>  POST: add a new news to the server
export function createNews(news) {
  let formData = new FormData();
  formData.append("active", news.active);
  formData.append("body", news.body);
  formData.append("type", document.type);
  formData.append("cover_image", news.cover_image);
  news.regions.forEach((item) => {
    formData.append("regions", item);
  });
  news.documents.forEach((item) => {
    formData.append("documents", item);
  });
  news.material_categories.forEach((item) => {
    formData.append("material_categories", item);
  });
  news.product_categories.forEach((item) => {
    formData.append("product_categories", item);
  });
  news.news_categories.forEach((item) => {
    formData.append("news_categories", item);
  });
  // since we removed organizations from news edit page
  //
  // news.organizations.forEach((item) => {
  //   formData.append("organizations", item);
  // });
  formData.append("pub_date", news.pub_date);
  news.regulations.forEach((item) => {
    formData.append("regulations", item);
  });
  news.regulatory_frameworks.forEach((item) => {
    formData.append("regulatory_frameworks", item);
  });
  formData.append("source", news.source);
  formData.append("status", news.status);
  formData.append("title", news.title);
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.post(NEWS_URL, formData, headers);
}

// READ
export function getNewsById(newsId) {
  return axios.get(`${NEWS_URL}${newsId}/`);
}

export function getNewsList(queryParams) {
  return axios.get(`${NEWS_URL}`, { params: queryParams });
}

export function getSourceList(queryParams) {
  return axios.get(`${NEWS_SOURCE}?pageSize=`);
}

export function getCategoryList(queryParams) {
  return axios.get(`${NEWS_CATEGORY}?pageSize=`);
}

// UPDATE => PUT: update the news on the server
export function updateNews(news) {
  const {
    title,
    status,
    source,
    active,
    body,
    pub_date,
    documents,
    material_categories,
    product_categories,
    news_categories,
    organizations,
    regulations,
    regulatory_frameworks,
    regions,
    review_comment,
    review_green,
    review_yellow,
  } = news;

  return axios.patch(`${NEWS_URL}${news.id}/`, {
    title,
    status,
    source,
    active,
    body,
    pub_date,
    documents,
    material_categories,
    product_categories,
    news_categories,
    organizations,
    regulations,
    regulatory_frameworks,
    regions,
    review_comment,
    review_green,
    review_yellow,
  }).then(() => {
    if (news.cover_image?.name) {
      let formData = new FormData();

      formData.append('cover_image', news.cover_image);
      formData.append('status', news.status);

      const headers = { 'Content-Type': 'multipart/form-data' };

      return axios.patch(`${NEWS_URL}${news.id}/`, formData, headers);
    }
  });
}

export function updateNewsDocuments({ newsId, documents }) {
  return axios.patch(`${NEWS_URL}${newsId}/`, { documents: documents });
}

// UPDATE => PATCH: update the news on the server
export function updateNewsPatch(id, news) {
  return axios.patch(`${NEWS_URL}${id}/`, news);
}

export function getRelevant(id, news) {
  return axios.post(`${NEWS_RELEVANT}`, news);
}

export function saveNewsFromDate(date) {
  return axios.get(`${NEWS_FROM_API}?from_date=${date}`);
}

// UPDATE Status
export function updateStatusForNews(ids, status) {
  return axios.post(`${NEWS_URL}updateStatusForNews`, { ids, status });
}

// DELETE => delete the news from the server
export function deleteNews(newsId) {
  return axios.delete(`${NEWS_URL}${newsId}/`);
}

// PATCH => to make the news discharged
export function dischargeNews(newsId) {
  return axios.patch(`${NEWS_URL}${newsId}/`, { 'status': 'd'});
}

export function getRegulationList() {
  return axios.get(REGULATION_URL);
}

export function getRegulatoryFrameworkList() {
  return axios.get(REGULATORY_FRAMEWORK_URL);
}

export function getProductCategoryList() {
  return axios.get(PRODUCT_CATEGORY_URL);
}

export function getMaterialCategoryList() {
  return axios.get(MATERIAL_CATEGORY_URL);
}

export function getOrganizationList() {
  return axios.get(ORGANIZATION_URL);
}

export function getDocumentList() {
  return axios.get(DOCUMENT_URL);
}

export function getNewsBodyDocs(newsId) {
  return axios.get(`${NEWS_URL}${newsId}/body_documents/`);
}

export function getIndustries() {
  return axios.get(INDUSTRIES_URL);
}

export function saveNewsDoc(newsId, doc) {
  return axios.post(`${NEWS_URL}${newsId}/save_document/`, doc);
}

// News related attachments or documents api

export function getDocumentTypeList() {
  return axios.get(`${DOCUMENT_TYPE_URL}?pazeSize=100`);
}

export function createNewsRelatedDocument(document) {
  let formData = new FormData();
  formData.append("title", document.title);
  formData.append("description", document.description);
  formData.append("type", document.type);
  formData.append("attachment", document.attachment);
  const headers = { "Content-Type": "multipart/form-data" };

  return axios.post(DOCUMENTS_URL, formData, headers);
}

export function updateNewsRelatedDocument(document) {
  let formData = new FormData();
  formData.append("title", document.title);
  formData.append("description", document.description);
  formData.append("type", document.type);

  if (document.attachment.name) {
    formData.append("attachment", document.attachment);
  }

  const headers = { "Content-Type": "multipart/form-data" };
  return axios.put(`${DOCUMENTS_URL}${document.id}/`, formData, headers);
}

//delete
export function deleteDocuments(documentID) {
  return axios.delete(`${DOCUMENTS_URL}${documentID}/`);
}

//News impact assessment

export function getNewsRelevanceList(queryParams) {
  return axios.get(`${RELEVANCE_URL}`, { params: queryParams });
}

export function saveNewsRelevance(relevance) {
  return axios.post(`${RELEVANCE_URL}`, relevance);
}

export function updateNewsRelevance(relevance) {
  return axios.put(`${RELEVANCE_URL}${relevance.id}/`, relevance);
}

export function deleteNewsRelevance(relevanceID) {
  return axios.delete(`${RELEVANCE_URL}${relevanceID}/`);
}

export function getRegionList() {
  return axios.get(REGION_URL);
}
