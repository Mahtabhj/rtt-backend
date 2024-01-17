import axios from "axios";

export const REGISTER_URL = "api/auth/register";
export const REQUEST_PASSWORD_URL = "api/auth/forgot-password";
const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
export const LOGIN_URL = BASE_URL + "token/";
export const ME_URL = BASE_URL + "users/me/";
export const PERMISSIONS_URL = BASE_URL + "user-permissions/";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

export function login(username, password) {
  return axios.post(LOGIN_URL, { username, password });
}

export function register(email, fullname, username, password) {
  return axios.post(REGISTER_URL, { email, fullname, username, password });
}

export function requestPassword(email) {
  return axios.post(REQUEST_PASSWORD_URL, { email });
}

export function getUserByToken() {
  return axios.get(ME_URL);
}

export function getUserPermissions() {
  return axios.get(PERMISSIONS_URL);
}
