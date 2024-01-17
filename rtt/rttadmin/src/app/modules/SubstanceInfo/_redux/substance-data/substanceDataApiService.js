import axios from 'axios';
import { isObject } from '@common';

const BASE_URL = `${process.env.REACT_APP_API_BASE_URI}api/`;
const SUBSTANCES_URL = `${BASE_URL}admin/substance-data/`;
const FILTERED_SUBSTANCES_IDS_URL = `${SUBSTANCES_URL}filtered-substance-data-list/`;
const EXISTING_SUBSTANCE_PROPERTY_DATA_POINTS_IDS_URL = `${SUBSTANCES_URL}property-data-point-options/`;
const PROPERTY_URL = `${SUBSTANCES_URL}property-options/`;
const ADD_SUBSTANCE_URL = SUBSTANCES_URL;
const UPDATE_SUBSTANCE_URL = SUBSTANCES_URL;
const DELETE_SUBSTANCE_URL = `${SUBSTANCES_URL}delete/`;
const UPLOAD_SUBSTANCE_URL = `${BASE_URL}es/substance/substances-upload/admin-substance-data/`;

export const getSubstanceData = queryParams => {
  return axios.get(`${SUBSTANCES_URL}`, { params: queryParams });
};

export const getFilteredSubstanceDataIdsList = queryParams => {
  return axios.get(`${FILTERED_SUBSTANCES_IDS_URL}`, { params: queryParams });
};

export const getExistingPoints = dataToSend => {
  return axios.post(`${EXISTING_SUBSTANCE_PROPERTY_DATA_POINTS_IDS_URL}`, dataToSend);
};

export const getPropertyList = () => {
  return axios.get(`${PROPERTY_URL}`);
};

export const addSubstanceData = dataToSend => {
  const formData = new FormData();
  formData.append('substance', dataToSend.substance);
  formData.append('property_data_point', dataToSend.property_data_point);
  formData.append('value', dataToSend.value);
  formData.append('status', dataToSend.status);
  formData.append('modified', dataToSend.modified);
  if (isObject(dataToSend.image)) {
    formData.append('image', dataToSend.image);
  } else if (dataToSend.image) {
    // save as new version url from response not changed
    formData.append('image_url', dataToSend.image);
  }
  const headers = { 'Content-Type': 'multipart/form-data' };
  return axios.post(ADD_SUBSTANCE_URL, formData, headers);
};

export const updateSubstanceData = (id, dataToSend) => {
  const formData = new FormData();
  formData.append('substance', dataToSend.substance);
  formData.append('property_data_point', dataToSend.property_data_point);
  formData.append('value', dataToSend.value);
  formData.append('status', dataToSend.status);
  formData.append('modified', dataToSend.modified);
  if (isObject(dataToSend.image)) formData.append('image', dataToSend.image);
  const headers = { 'Content-Type': 'multipart/form-data' };
  return axios.patch(`${UPDATE_SUBSTANCE_URL}${id}/`, formData, headers);
};

export const deleteSubstanceData = dataToSend => {
  return axios.post(`${DELETE_SUBSTANCE_URL}`, dataToSend);
};

export function uploadSubstanceData(file) {
  const formData = new FormData();
  formData.append('file', file);

  return axios.post(`${UPLOAD_SUBSTANCE_URL}`, formData, { 'Content-Type': 'multipart/form-data' });
}
