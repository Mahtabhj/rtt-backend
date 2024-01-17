import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const ORGANIZATION_URL = BASE_URL + "issuing-body/";
const REGION_URL = BASE_URL + "region/";
const URLS_URL = BASE_URL + "url/";

// CREATE =>  POST: add a new issuingbody to the server
export function createIssuingBody(issuingbody) {
  return axios.post(ORGANIZATION_URL, issuingbody);
}

export function getRegionList() {
  return axios.get(REGION_URL);
}

// READ
export function getAllIssuingBody() {
  let result = axios.get(ORGANIZATION_URL);
  return result;
}

export function getIssuingBodyById(issuingbodyId) {
  return axios.get(`${ORGANIZATION_URL}${issuingbodyId}/`);
}

export function getIssuingBodyList(queryParams) {
  return axios.get(`${ORGANIZATION_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the issuingbody on the server
export function updateIssuingBody(issuingbody) {
  return axios.put(`${ORGANIZATION_URL}${issuingbody.id}/`, issuingbody);
}

// UPDATE Status
export function updateStatusForIssuingBody(ids, status) {
  return axios.post(`${ORGANIZATION_URL}updateStatusForIssuingBody`, {
    ids,
    status,
  });
}

// DELETE => delete the issuingbody from the server
export function deleteIssuingBody(issuingbodyId) {
  return axios.delete(`${ORGANIZATION_URL}${issuingbodyId}/`);
}

export function getURLsList() {
  return axios.get(URLS_URL);
}
