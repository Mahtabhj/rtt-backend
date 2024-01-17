import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const IMPACT_ASSESSMENT_LIST_URL = BASE_URL + "impact-assessments/";
const IMPACT_ASSESSMENT_ANSWER_URL = BASE_URL + "impact-assessment-answer/";
const USERS_URL = BASE_URL + "users/";

// Regulation Impact Assessment

export function getImpactAssessmentList(queryParams) {
  return axios.get(`${IMPACT_ASSESSMENT_LIST_URL}`, { params: queryParams });
}

export function getImpactAssessmentAnswers() {
  return axios.get(`${IMPACT_ASSESSMENT_ANSWER_URL}?pageSize=`);
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

export function getUserList(queryParams) {
  return axios.get(`${USERS_URL}`, { queryParams });
}
