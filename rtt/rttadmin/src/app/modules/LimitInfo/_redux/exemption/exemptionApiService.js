import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const EXEMPTIONS_URL = BASE_URL + "admin/exemption/";
const FILTERED_EXEMPTIONS_IDS_URL = BASE_URL + "admin/exemption/filtered-exemption-list/";
const ADD_EXEMPTION_URL = BASE_URL + "admin/exemption/";
const DELETE_EXEMPTION_URL = BASE_URL + "admin/exemption/delete-exemption/";
const UPDATE_EXEMPTION_URL = BASE_URL + "admin/exemption/";
const UPLOAD_EXEMPTION_URL = BASE_URL + "limit/limit-upload/exemption/";

export const getExemptionsList = queryParams => {
  return axios.get(`${EXEMPTIONS_URL}`, { params: queryParams });
}

export const getFilteredExemptionsIdsList = queryParams => {
  return axios.get(`${FILTERED_EXEMPTIONS_IDS_URL}`, { params: queryParams });
}

export const addExemption = dataToSend => {
  return axios.post(`${ADD_EXEMPTION_URL}`, dataToSend);
}

export const deleteExemption = dataToSend => {
  return axios.post(`${DELETE_EXEMPTION_URL}`, dataToSend);
}

export const updateExemption = (id, dataToSend) => {
  return axios.patch(`${UPDATE_EXEMPTION_URL}${id}/`, dataToSend);
}

export function uploadExemptions(file) {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${UPLOAD_EXEMPTION_URL}`, formData, { 'Content-Type': 'multipart/form-data' });
}
