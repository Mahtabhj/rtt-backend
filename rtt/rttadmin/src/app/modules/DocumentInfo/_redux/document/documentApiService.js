import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const DOCUMENT_URL = BASE_URL + "documents/";

// CREATE =>  POST: add a new document to the server
export function createDocument(document) {
  let formData = new FormData();
  formData.append("title", document.title);
  formData.append("type", document.type);
  formData.append("description", document.description);
  formData.append("attachment", document.attachment);
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.post(DOCUMENT_URL, formData, headers);
}

// READ
export function getAllDocument() {
  return axios.get(DOCUMENT_URL);
}

export function getDocumentById(documentId) {
  return axios.get(`${DOCUMENT_URL}${documentId}/`);
}

export function getDocumentList(queryParams) {
  return axios.get(`${DOCUMENT_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the document on the server
export function updateDocument(document) {
  let formData = new FormData();
  formData.append("id", document.id);
  formData.append("title", document.title);
  formData.append("type", document.type.id);
  formData.append("description", document.description);
  if (document.attachment.name) {
    formData.append("attachment", document.attachment);
  }
  const headers = { "Content-Type": "multipart/form-data" };
  let response = axios.put(`${DOCUMENT_URL}${document.id}/`, formData, headers);
  return response;
}

// UPDATE Status
export function updateStatusForDocument(ids, status) {
  return axios.post(`${DOCUMENT_URL}updateStatusForDocument`, {
    ids,
    status,
  });
}

// DELETE => delete the document from the server
export function deleteDocument(documentId) {
  return axios.delete(`${DOCUMENT_URL}${documentId}/`);
}

// todo use commonApi
export function getDocumentTypeList() {
  return axios.get(BASE_URL + "document-type/?pageSize=");
}
