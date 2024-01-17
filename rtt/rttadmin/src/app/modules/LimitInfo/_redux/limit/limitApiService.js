import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const LIMITS_URL = BASE_URL + "admin/limit/";
const FILTERED_LIMITS_IDS_URL = BASE_URL + "admin/limit/filtered-limit-list/";
const LIMIT_ATTRIBUTES_URL = BASE_URL + "limit/attribute-options/";
const ADD_LIMIT_URL = BASE_URL + "admin/limit/";
const DELETE_LIMIT_URL = BASE_URL + "admin/limit/delete-limit/";
const UPDATE_LIMIT_URL = BASE_URL + "admin/limit/update-limit/";
const UPLOAD_LIMIT_URL = BASE_URL + "limit/limit-upload/limit_with_additional_attribute_value/";

export const getLimitsList = queryParams => {
  return axios.get(`${LIMITS_URL}`, { params: queryParams });
}

export const getFilteredLimitsIdsList = queryParams => {
  return axios.get(`${FILTERED_LIMITS_IDS_URL}`, { params: queryParams });
}

export const getLimitAttributesList = queryParams => {
  return axios.post(`${LIMIT_ATTRIBUTES_URL}`, queryParams);
}

export const addLimit = dataToSend => {
  return axios.post(`${ADD_LIMIT_URL}`, dataToSend);
}

export const deleteLimit = dataToSend => {
  return axios.post(`${DELETE_LIMIT_URL}`, dataToSend);
}

export const updateLimit = dataToSend => {
  return axios.post(`${UPDATE_LIMIT_URL}`, dataToSend);
}

export function uploadLimits(file) {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${UPLOAD_LIMIT_URL}`, formData, { 'Content-Type': 'multipart/form-data' });
}