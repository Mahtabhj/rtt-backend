import axios from 'axios';

const BASE_URL = `${process.env.REACT_APP_API_BASE_URI}api/`;
const DOCUMENT_TYPES_URL = `${BASE_URL}document-type/`;
const INDUSTRY_URL = `${BASE_URL}industries/`;
const ISSUE_URL = `${BASE_URL}issuing-body/`;
const REGULATION_URL = `${BASE_URL}regulation/`;
const REGULATION_DROPDOWN_URL = `${BASE_URL}regulation/dropdown-data/`;
const FRAMEWORK_DROPDOWN_URL = `${BASE_URL}regulatory-framework/dropdown-data/`;
const SUBSTANCE_DROPDOWN_URL = `${BASE_URL}admin/all-substance-list/`;
const RELEVANT_ORGANIZATIONS = `${BASE_URL}organizations/get_relevant_organizations/`;

export const getDocumentTypeList = () => axios.get(`${DOCUMENT_TYPES_URL}`);

export const getIndustryList = () => axios.get(INDUSTRY_URL);

export const getIssuingBodyDropdownData = keyword =>
  axios.get(ISSUE_URL, {
    params: {
      search: keyword,
    },
  });

export const getRegulationDropdownData = keyword =>
  axios.get(`${REGULATION_DROPDOWN_URL}`, {
    params: {
      search: keyword,
    },
  });

export const getSubstancesDropdownData = keyword =>
  axios.post(`${SUBSTANCE_DROPDOWN_URL}`, {
    search: keyword,
  });

export const getFrameworkDropdownData = keyword =>
  axios.get(`${FRAMEWORK_DROPDOWN_URL}`, {
    params: {
      search: keyword,
    },
  });

export const getRegulationDetailById = regulationId => axios.get(`${REGULATION_URL}${regulationId}/details/`);

export const getRelevantOrganizations = payload => axios.post(`${RELEVANT_ORGANIZATIONS}`, payload);
