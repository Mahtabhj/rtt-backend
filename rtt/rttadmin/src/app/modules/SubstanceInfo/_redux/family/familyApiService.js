import axios from 'axios';

const BASE_URL = `${process.env.REACT_APP_API_BASE_URI}api`;
const FAMILY_URL = `${BASE_URL}/admin/substance-family`;
const UPLOAD_FAMILY_SUBSTANCES_URL = `${BASE_URL}/es/substance/substances-upload/admin-substance-families`;

export const getFamilies = queryParams => axios.get(`${FAMILY_URL}/`, { params: queryParams });

export const addFamily = dataToSend => axios.post(`${FAMILY_URL}/`, dataToSend);

export const getEditFamily = id => axios.get(`${FAMILY_URL}/${id}/`);

export const updateFamily = (id, dataToSend) => axios.patch(`${FAMILY_URL}/${id}/`, dataToSend);

export const deleteFamily = id => axios.post(`${FAMILY_URL}/${id}/delete/`);

export const getSubstances = (id, dataToSend) => axios.post(`${FAMILY_URL}/${id}/tagged-substances/`, dataToSend);

export const getFilteredSubstancesIdsList = (id, dataToSend) =>
  axios.post(`${FAMILY_URL}/${id}/all-tagged-substances-id/`, dataToSend);

export const addFamilySubstances = (id, substances) =>
  axios.post(`${FAMILY_URL}/${id}/add-or-remove-substance/`, { substances, action: 'add' });

export const deleteFamilySubstances = (id, substances) =>
  axios.post(`${FAMILY_URL}/${id}/add-or-remove-substance/`, { substances, action: 'remove' });

export const uploadFamilySubstances = (file, familyId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('family_id', familyId);

  return axios.post(`${UPLOAD_FAMILY_SUBSTANCES_URL}/`, formData, { 'Content-Type': 'multipart/form-data' });
};
