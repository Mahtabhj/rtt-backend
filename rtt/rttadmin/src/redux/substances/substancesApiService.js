import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const RELATED_SUBSTANCES_URL = BASE_URL + "related-substance-list/";
const ADD_OR_REMOVE_SUBSTANCES_URL = BASE_URL + "substance/manual-add-or-remove-relation/";
const ADD_SUBSTANCES_UPLOAD_URL = BASE_URL + "substance/upload-substance-add-relation/";

export function getRelatedSubstancesPaginated(queryParams) {
  return axios.post(`${RELATED_SUBSTANCES_URL}`, { ...queryParams });
}

export function addOrRemoveSubstances(dataToSend) {
  return axios.post(`${ADD_OR_REMOVE_SUBSTANCES_URL}`, { ...dataToSend });
}

export function addSubstanceUpload(formData, config) {
  return axios.post(`${ADD_SUBSTANCES_UPLOAD_URL}`, formData, { ...config });
}