import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const INDUSTRY_URL = BASE_URL + "industries/";

// CREATE =>  POST: add a new industry to the server
export function createIndustry(industry) {
  return axios.post(INDUSTRY_URL, industry);
}

// READ
export function getAllIndustry() {
  return axios.get(INDUSTRY_URL);
}

export function getIndustryById(industryId) {
  return axios.get(`${INDUSTRY_URL}${industryId}/`);
}

export function getIndustryList(queryParams) {
  return axios.get(`${INDUSTRY_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the industry on the server
export function updateIndustry(industry) {
  return axios.put(`${INDUSTRY_URL}${industry.id}/`, industry);
}

// UPDATE Status
export function updateStatusForIndustry(ids, status) {
  return axios.post(`${INDUSTRY_URL}updateStatusForIndustry`, {
    ids,
    status,
  });
}

// DELETE => delete the industry from the server
export function deleteIndustry(industryId) {
  return axios.delete(`${INDUSTRY_URL}${industryId}/`);
}
