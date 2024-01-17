import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const REGULATORY_FRAMEWORK_URL = BASE_URL + "regulatory-framework/";
const LANGUAGE_URL = BASE_URL + "language/";
const STATUS_URL = BASE_URL + "status/";
const REGION_URL = BASE_URL + "region/";
const REGULATION_URL = BASE_URL + "regulation/";
const LINK_URL = BASE_URL + "url/";
const MILESTONE_URL = BASE_URL + "milestone/";
const MILESTONE_TYPE_URL = BASE_URL + "milestone-type/";
const REGULATORY_FRAMEWORK_LINK_URL = BASE_URL + "reg-framework-url/";
const REGULATION_TYPE_URL = BASE_URL + "regulation-type/";
const PRODUCT_CATEGORIES = BASE_URL + "product-categories/";
const MATERIAL_CATEGORIES = BASE_URL + "material-categories/";
const USERS_URL = BASE_URL + "users/";
const IMPACT_ASSESSMENT_URL = BASE_URL + "impact-assessment/";
const DOCUMENT_TYPES_URL = BASE_URL + "document-type/";
const DOCUMENTS_URL = BASE_URL + "documents/";
const IMPACT_ASSESSMENT_ANSWER_URL = BASE_URL + "impact-assessment-answer/";
const TOPIC_URL = BASE_URL + "topic/";

// CREATE =>  POST: add a new regulatoryFramework to the server
export function createRegulatoryFramework(regulatoryFramework) {
  return axios.post(REGULATORY_FRAMEWORK_URL, regulatoryFramework);
}

export function createRegulatoryFrameworkRelatedRegulation(regulation) {
  return axios.post(REGULATION_URL, regulation);
}

export function createRegulatoryFrameworkLink(link) {
  return axios.post(REGULATORY_FRAMEWORK_LINK_URL, link);
}
// READ
export function getAllRegulatoryFramework() {
  return axios.get(REGULATORY_FRAMEWORK_URL);
}
export function getAllTopicsList() {
  return axios.get(`${TOPIC_URL}?pageSize=`);
}

export function getRegulatoryFrameworkById(regulatoryFrameworkId) {
  return axios.get(`${REGULATORY_FRAMEWORK_URL}${regulatoryFrameworkId}/`);
}

export function getRegulatoryFrameworkList(queryParams) {
  return axios.get(`${REGULATORY_FRAMEWORK_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the regulatoryFramework on the server
export function updateRegulatoryFramework(regulatoryFramework) {
  return axios.put(
    `${REGULATORY_FRAMEWORK_URL}${regulatoryFramework.id}/`,
    regulatoryFramework
  );
}

// UPDATE Status
export function updateStatusForRegulatoryFramework(ids, status) {
  return axios.post(`${REGULATORY_FRAMEWORK_URL}updateStatusForRegulatoryFramework`, {
    ids,
    status,
  });
}

export function updateRegulatoryFrameworkLink(link) {
  return axios.put(`${LINK_URL}${link.id}/`, link);
}

// DELETE => delete the regulatoryFramework from the server
export function deleteRegulatoryFramework(regulatoryFrameworkId) {
  return axios.delete(`${REGULATORY_FRAMEWORK_URL}${regulatoryFrameworkId}/`);
}

export function deleteRegulatoryFrameworkRelatedRegulation(
  regulatoryFrameworkId
) {
  return axios.delete(`${REGULATION_URL}${regulatoryFrameworkId}/`);
}

export function deleteLink(linkID) {
  return axios.delete(`${LINK_URL}${linkID}/`);
}

export function getLanguageList() {
  return axios.get(`${LANGUAGE_URL}?pageSize=`);
}

export function getStatusList() {
  return axios.get(`${STATUS_URL}?pageSize=`);
}

export function getRegionList() {
  return axios.get(`${REGION_URL}?pageSize=`);
}

export function getRelatedRegulationList(queryParams) {
  return axios.get(`${REGULATION_URL}`, {
    params: { rf_id: queryParams },
  });
}

// export function getRegulatoryFrameworkRelatedRegulationById(regulationId) {
//   return axios.get(`${REGULATION_URL}${regulationId}/`);
// }

// UPDATE => PATCH: update the regulatory framework field on the server
export function updateRegulatoryFrameworkField(regulatoryFramework) {
  return axios.patch(`${REGULATORY_FRAMEWORK_URL}${regulatoryFramework.id}/`, regulatoryFramework);
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
    params: { rf_id: queryParams },
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

export function getRegulationTypeList() {
  return axios.get(`${REGULATION_TYPE_URL}?pageSize=`);
}

export function getUserList(queryParams) {
  return axios.get(USERS_URL, { params: queryParams });
}

export function getMaterialCategoryList(queryParams) {
  return axios.get(MATERIAL_CATEGORIES, { params: queryParams });
}

export function getProductCategoryList(queryParams) {
  return axios.get(PRODUCT_CATEGORIES, { params: queryParams });
}

export function getLinkList() {
  return axios.get(`${LINK_URL}?pageSize=`);
}

// Regulatory framework Impact Assessment

export function getRegulatoryFrameworkImpactAssessmentById(
  regulatoryFrameworkId
) {
  return axios.get(`${IMPACT_ASSESSMENT_URL}?rf_id=${regulatoryFrameworkId}`);
}

export function getRegulatoryFrameworkImpactAssessmentAnswers(framework_id) {
  return axios.get(
    `${IMPACT_ASSESSMENT_ANSWER_URL}?framework_id=${framework_id}&pageSize=1000`
  );
}

//create
export function createRegulatoryFrameworkImpactAssessment(impactAssessment) {
  return axios.post(IMPACT_ASSESSMENT_URL, impactAssessment);
}

//update
export function updateRegulatoryFrameworkImpactAssessment(impactAssessment) {
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

// Regulatory framework related attachments or documents api

// todo common api
export function getDocumentTypeList() {
  return axios.get(DOCUMENT_TYPES_URL);
}

export function createRegulatoryFrameworkRelatedDocument(document) {
  let formData = new FormData();
  formData.append("title", document.title);
  formData.append("description", document.description);
  formData.append("type", document.type);
  formData.append("attachment", document.attachment);
  const headers = { "Content-Type": "multipart/form-data" };

  return axios.post(DOCUMENTS_URL, formData, headers);
}

export function updateRegulatoryFrameworkRelatedDocument(document) {
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

export function updateRegulatoryFrameworkDocuments({
  regulatoryFrameworkId,
  documents,
}) {
  return axios.patch(`${REGULATORY_FRAMEWORK_URL}${regulatoryFrameworkId}/`, {
    documents: documents,
  });
}

//delete
export function deleteDocuments(documentID) {
  return axios.delete(`${DOCUMENTS_URL}${documentID}/`);
}

export function getDocumentsList(queryParams) {
  return axios.get(DOCUMENTS_URL, { params: queryParams });
}

export function createUrl(url) {
  return axios.post(LINK_URL, url);
}

export function updateUrl(url) {
  return axios.put(`${LINK_URL}${url.id}/`, url);
}

export function getRegulatoryFrameworkRelevantOrganizations(payload) {
  return axios.post(`${REGULATORY_FRAMEWORK_URL}get_relevant_organizations/`, payload);
}