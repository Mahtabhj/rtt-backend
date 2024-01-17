import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const DOCUMENT_URL = BASE_URL + "news-source/";
const SOURCE_TYPE_URL = BASE_URL + "source-type/";

// CREATE =>  POST: add a new source to the server
export function createSource(source) {
  let formData = new FormData();
  formData.append("name", source.name);
  formData.append("link", source.link);
  formData.append("description", source.description);
  formData.append("image", source.image);
  formData.append("type", source.type);
  const headers = { "Content-Type": "multipart/form-data" };

  return axios.post(DOCUMENT_URL, formData, headers);
}

// READ
export function getAllSource() {
  return axios.get(DOCUMENT_URL);
}

export function getSourceById(sourceId) {
  return axios.get(`${DOCUMENT_URL}${sourceId}/`);
}

export function getSourceTypeList() {
  return axios.get(`${SOURCE_TYPE_URL}?pageSize=`);
}

export function getSourceList(queryParams) {
  return axios.get(`${DOCUMENT_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the source on the server
export function updateSource(source) {
  let formData = new FormData();
  formData.append("id", source.id);
  formData.append("name", source.name);
  formData.append("link", source.link);
  formData.append("description", source.description);
  if (source.image && source.image.name !== undefined) {
    formData.append("image", source.image);
  }
  formData.append("type", source.type);
  const headers = { "Content-Type": "multipart/form-data" };
  let response = axios.put(`${DOCUMENT_URL}${source.id}/`, formData, headers);
  return response;
}

// UPDATE Status
export function updateStatusForSource(ids, status) {
  return axios.post(`${DOCUMENT_URL}updateStatusForSource`, {
    ids,
    status,
  });
}

// DELETE => delete the source from the server
export function deleteSource(sourceId) {
  return axios.delete(`${DOCUMENT_URL}${sourceId}/`);
}
