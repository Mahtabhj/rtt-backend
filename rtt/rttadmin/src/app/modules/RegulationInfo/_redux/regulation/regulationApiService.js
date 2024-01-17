import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const REGULATION_URL = BASE_URL + "regulation/";
const REGULATION_TYPE_URL = BASE_URL + "regulation-type/";
const LANGUAGE_URL = BASE_URL + "language/";
const STATUS_URL = BASE_URL + "status/";
const REGULATORY_FRAMEWORK_URL = BASE_URL + "regulatory-framework/";
const DOCUMENTS_URL = BASE_URL + "documents/";
const MATERIAL_CATEGORIES_URL = BASE_URL + "material-categories/";
const PRODUCT_CATEGORIES_URL = BASE_URL + "product-categories/";
const LINK_URL = BASE_URL + "url/";
const USERS_URL = BASE_URL + "users/";
const IMPACT_ASSESSMENT_URL = BASE_URL + "impact-assessment/";
const IMPACT_ASSESSMENT_ANSWER_URL = BASE_URL + "impact-assessment-answer/";
const MILESTONE_URL = BASE_URL + "milestone/";
const MILESTONE_TYPE_URL = BASE_URL + "milestone-type/";
const TOPIC_URL = BASE_URL + "topic/";

// CREATE =>  POST: add a new regulation to the server
export function createRegulation(regulation) {
  return axios.post(REGULATION_URL, regulation);
}

//READ => All regulation types list
export function getRegulationTypeList() {
  return axios.get(`${REGULATION_TYPE_URL}?pageSize=`);
}

//READ => All languages list
export function getLanguageList() {
  return axios.get(`${LANGUAGE_URL}?pageSize=`);
}

//READ => All status list
export function getStatusList() {
  return axios.get(`${STATUS_URL}?pageSize=`);
}

//READ => All regulatory framework list
export function getRegulatoryFrameworkList(params) {
  return axios.get(REGULATORY_FRAMEWORK_URL, { params });
}

//READ => All documents list
export function getDocumentsList(queryParams) {
  return axios.get(DOCUMENTS_URL, { params: queryParams });
}

export function getAllTopicsList() {
  return axios.get(`${TOPIC_URL}?pageSize=`);
}

export function getUserList(queryParams) {
  return axios.get(`${USERS_URL}`, { queryParams });
}

//READ => All material categories list
export function getMaterialCategoriesList(queryParams) {
  return axios.get(MATERIAL_CATEGORIES_URL, { params: queryParams });
}

//READ => All product categories list
export function getProductCategoriesList(queryParams) {
  return axios.get(PRODUCT_CATEGORIES_URL, { params: queryParams });
}

//READ => All urls list
export function getURLsList() {
  return axios.get(`${LINK_URL}?pageSize=`);
}

export function getRegulationById(regulationId) {
  return axios.get(`${REGULATION_URL}${regulationId}/`);
}

export function getRegulationList(queryParams) {
  return axios.get(`${REGULATION_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the regulation on the server
export function updateRegulation(regulation) {
  return axios.put(`${REGULATION_URL}${regulation.id}/`, regulation);
}

// UPDATE => PATCH: update the regulation field on the server
export function updateRegulationField(regulation) {
  return axios.patch(`${REGULATION_URL}${regulation.id}/`, regulation);
}

// UPDATE Status
export function updateStatusForRegulation(ids, status) {
  return axios.post(`${REGULATION_URL}updateStatusForRegulation`, {
    ids,
    status,
  });
}

// UPDATE urls
export function updateUrlsForRegulation(ids, status) {
  return axios.post(`${REGULATION_URL}updateStatusForRegulation`, {
    ids,
    status,
  });
}

// DELETE => delete the regulation from the server
export function deleteRegulation(regulationId) {
  return axios.delete(`${REGULATION_URL}${regulationId}/`);
}

//Related URLs table

//create
export function createRegulationUrl(url) {
  return axios.post(LINK_URL, url);
}

//update
export function updateRegulationUrl(url) {
  return axios.put(`${LINK_URL}${url.id}/`, url);
}

//delete
export function deleteUrl(urlID) {
  return axios.delete(`${LINK_URL}${urlID}/`);
}

// Regulation related attachments or documents api

export function createRegulationRelatedDocument(document) {
  let formData = new FormData();
  formData.append("title", document.title);
  formData.append("description", document.description);
  formData.append("type", document.type);
  formData.append("attachment", document.attachment);
  const headers = { "Content-Type": "multipart/form-data" };

  return axios.post(DOCUMENTS_URL, formData, headers);
}

export function updateRegulationRelatedDocument(document) {
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

// Regulation Impact Assessment

export function getRegulationImpactAssessmentById(regulationId) {
  return axios.get(`${IMPACT_ASSESSMENT_URL}?r_id=${regulationId}`);
}

export function getRegulationImpactAssessmentAnswers(regulation_id) {
  return axios.get(
    `${IMPACT_ASSESSMENT_ANSWER_URL}?regulation_id=${regulation_id}&pageSize=1000`
  );
}

//create
export function createRegulationImpactAssessment(impactAssessment) {
  return axios.post(IMPACT_ASSESSMENT_URL, impactAssessment);
}

//update
export function updateRegulationImpactAssessment(impactAssessment) {
  return axios.put(
    `${IMPACT_ASSESSMENT_URL}${impactAssessment.id}/`,
    impactAssessment
  );
}

//delete
export function deleteImpactAssessment(impactAssessmentID) {
  return axios.delete(`${IMPACT_ASSESSMENT_URL}${impactAssessmentID}/`);
}

//update answers
export function updateImpactAssessmentAnswers(ans) {
  if (ans) {
    if (!ans.id) {
      return axios.post(IMPACT_ASSESSMENT_ANSWER_URL, ans);
    } else {
      return axios.put(`${IMPACT_ASSESSMENT_ANSWER_URL}${ans.id}/`, ans);
    }
  }
}

// Related Milestones API

export function createRelatedMilestone(milestone) {
  return axios.post(MILESTONE_URL, milestone);
}

export function updateRelatedMilestone(milestone) {
  return axios.put(`${MILESTONE_URL}${milestone.id}/`, milestone);
}

export function getRelatedMilestoneList(queryParams) {
  return axios.get(`${MILESTONE_URL}?pageSize=`, {
    params: { r_id: queryParams },
  });
}

export function getRelatedMilestoneById(milestoneId) {
  return axios.get(`${MILESTONE_URL}${milestoneId}/`);
}

export function getMilestoneTypeList() {
  return axios.get(`${MILESTONE_TYPE_URL}?pageSize=`);
}

export function deleteRelatedMilestone(id) {
  return axios.delete(`${MILESTONE_URL}${id}/`);
}

export function getRegulationRelevantOrganizations(payload) {
  return axios.post(`${REGULATION_URL}get_relevant_organizations/`, payload);
}