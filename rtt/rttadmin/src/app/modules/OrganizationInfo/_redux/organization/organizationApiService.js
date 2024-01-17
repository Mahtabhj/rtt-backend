import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const ORGANIZATION_URL = BASE_URL + "organizations/";
const USER_URL = BASE_URL + "users/";
const SUBSCRIPTION_URL = BASE_URL + "subscriptions/";
const SUBSCRIPTION_TYPES_URL = BASE_URL + "subscription-type/";

export function createOrganization(organization) {
  let formData = new FormData();
  formData.append("name", organization.name);
  formData.append("country", organization.country);
  formData.append("address", organization.address);
  formData.append("tax_code", organization.tax_code);
  formData.append("active", organization.active);
  formData.append("description", organization.description);
  formData.append("primary_color", organization.primary_color);
  formData.append("secondary_color", organization.secondary_color);
  formData.append("session_timeout", organization.session_timeout);
  formData.append("password_expiration", organization.password_expiration);
  formData.append("logo", organization.logo);
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.post(ORGANIZATION_URL, formData, headers);
}

export function updateOrganization(organization) {
  let formData = new FormData();
  formData.append("name", organization.name);
  formData.append("country", organization.country);
  formData.append("address", organization.address);
  formData.append("tax_code", organization.tax_code);
  formData.append("active", organization.active);
  formData.append("description", organization.description);
  formData.append("primary_color", organization.primary_color);
  formData.append("secondary_color", organization.secondary_color);
  formData.append("session_timeout", organization.session_timeout);
  formData.append("password_expiration", organization.password_expiration);
  if (organization.logo.name) {
    formData.append("logo", organization.logo);
  }
  const headers = { "Content-Type": "multipart/form-data" };
  let response = axios.put(
    `${ORGANIZATION_URL}${organization.id}/`,
    formData,
    headers
  );
  return response;
}

// CREATE =>  POST: add a new organization user to the server
export function createOrganizationUser(user) {
  return axios.post(USER_URL, user);
}

// CREATE =>  POST: add a new organization subscription
export function createOrganizationSubscription(subscription) {
  return axios.post(SUBSCRIPTION_URL, subscription);
}

// READ
export function getAllOrganization() {
  return axios.get(ORGANIZATION_URL);
}

export function getOrganizationById(organizationId) {
  return axios.get(`${ORGANIZATION_URL}${organizationId}/`);
}

export function getOrganizationList(params) {
  return axios.get(`${ORGANIZATION_URL}`, { params });
}

// UPDATE => PUT: update the organization on the server
export function updateOrganizationUser(user) {
  return axios.put(`${USER_URL}${user.id}/`, user);
}

export function changePassword(data) {
  return axios.put(`${USER_URL}change-organization-user-password/`, data);
}

export function updateOrganizationSubscription(subscription) {
  return axios.put(`${SUBSCRIPTION_URL}${subscription.id}/`, subscription);
}

// UPDATE Status
export function updateStatusForOrganization(ids, status) {
  return axios.post(`${ORGANIZATION_URL}updateStatusForOrganization`, {
    ids,
    status,
  });
}

// DELETE => delete the organization from the server
export function deleteOrganization(organizationId) {
  return axios.delete(`${ORGANIZATION_URL}${organizationId}/`);
}

export function deleteOrganizationUser(userId) {
  return axios.delete(`${USER_URL}${userId}/`);
}

export function deleteOrganizationSubscription(subscriptionId) {
  return axios.delete(`${SUBSCRIPTION_URL}${subscriptionId}/`);
}

export function getOrganizationUserList(queryParams) {
  return axios.get(`${USER_URL}`, {
    params: { organization_id: queryParams, pageSize: 1000 },
  });
}

export function getOrganizationSubscriptionList(queryParams) {
  return axios.get(`${SUBSCRIPTION_URL}`, {
    params: { organization_id: queryParams },
  });
}

export function getOrganizationSubscriptionTypes() {
  return axios.get(SUBSCRIPTION_TYPES_URL);
}

export function getOrganizationUserById(userId) {
  return axios.get(`${USER_URL}${userId}/`);
}

export function getOrganizationSubscriptionById(subscriptionId) {
  return axios.get(`${SUBSCRIPTION_URL}${subscriptionId}/`);
}
