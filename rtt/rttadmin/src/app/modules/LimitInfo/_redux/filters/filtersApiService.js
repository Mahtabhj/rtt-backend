import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URI + 'api/';
const REGULATION_OPTIONS_URL = BASE_URL + 'regulation/options/';
const REGULATORY_FRAMEWORK_OPTIONS_URL = BASE_URL + 'regulatory-framework/options/';
const REGION_OPTIONS_URL = BASE_URL + 'region/options/';

export const getRegulationFilter = keyword => {
  return axios.get(`${REGULATION_OPTIONS_URL}`, { params: { search: keyword } });
}

export const getRegulatoryFrameworkFilter = keyword => {
  return axios.get(`${REGULATORY_FRAMEWORK_OPTIONS_URL}`, { params: { search: keyword } });
}

export const getRegionFilter = keyword => {
  return axios.get(`${REGION_OPTIONS_URL}`, { params: { search: keyword } });
}
