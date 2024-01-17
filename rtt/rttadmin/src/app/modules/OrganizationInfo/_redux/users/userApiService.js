import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
export const USERS_URL = BASE_URL + "users/";
const ORGANIZATION_URL = BASE_URL + "organizations/";

// CREATE =>  POST: add a new user to the server
export function createUser(user) {
  return axios.post(USERS_URL, user);
}

// READ
export function getAllUsers() {
  return axios.get(USERS_URL);
}

export function getOrganizationList(queryParams) {
  return axios.get(`${ORGANIZATION_URL}`, { params: queryParams });
}

export function getUserById(userId) {
  return axios.get(`${USERS_URL}${userId}/`);
}

export function findUsers(params) {
  return axios.get(USERS_URL, { params });
}

// UPDATE => PUT: update the user on the server
export function updateUser(user) {
  return axios.put(`${USERS_URL}${user.id}/`, user);
}

// UPDATE Status
export function updateStatusForUsers(ids, status) {
  return axios.post(`${USERS_URL}updateStatusForUsers`, {
    ids,
    status,
  });
}

// DELETE => delete the user from the server
export function deleteUser(userId) {
  return axios.delete(`${USERS_URL}${userId}/`);
}

// DELETE Users by ids
export function deleteUsers(ids) {
  return axios.post(`${USERS_URL}deleteUsers`, { ids });
}
