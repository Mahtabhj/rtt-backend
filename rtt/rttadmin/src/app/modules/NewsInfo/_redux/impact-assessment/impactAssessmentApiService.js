import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const IMPACT_ASSESSMENT_LIST_URL = BASE_URL + "news-assessment-workflow/";
const IMPACT_ASSESSMENT_QUESTIONS_URL = BASE_URL + "news-impact-assessment-question/";
const ADD_IMPACT_ASSESSMENT_ANSWERS_URL = BASE_URL + "bulk-add-new-assessment/";

// News Impact Assessment
export function getImpactAssessmentList(queryParams) {
  return axios.get(`${IMPACT_ASSESSMENT_LIST_URL}`, { params: queryParams });
}

export function getImpactAssessmentById(newsId) {
  return axios.get(`${IMPACT_ASSESSMENT_LIST_URL}${newsId}/`);
}

export function getImpactAssessmentQuestions(organizationId) {
  return axios.get(`${IMPACT_ASSESSMENT_QUESTIONS_URL}`, {
    params: {
      organization: organizationId
    }
  });
}

export function addImpactAssessmentAnswers(newsId, dataToSend) {
  return axios.post(`${ADD_IMPACT_ASSESSMENT_ANSWERS_URL}${newsId}/`, dataToSend);
}
