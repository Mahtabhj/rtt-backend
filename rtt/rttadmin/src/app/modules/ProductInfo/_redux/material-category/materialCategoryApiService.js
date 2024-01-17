import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const INDUSTRY_URL = BASE_URL + "material-categories/";

// CREATE =>  POST: add a new materialCategory to the server
export function createMaterialCategory(materialCategory) {
  let formData = new FormData();
  formData.append("name", materialCategory.name);
  formData.append("description", materialCategory.description);
  formData.append("online", materialCategory.online);
  formData.append("image", materialCategory.image);
  formData.append("industry", materialCategory.industry);
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.post(INDUSTRY_URL, formData, headers);
}

// READ
export function getAllMaterialCategory() {
  return axios.get(INDUSTRY_URL);
}

export function getMaterialCategoryById(materialCategoryId) {
  return axios.get(`${INDUSTRY_URL}${materialCategoryId}/`);
}

export function getMaterialCategoryList(queryParams) {
  return axios.get(`${INDUSTRY_URL}`, { params: queryParams });
}

// UPDATE => PUT: update the materialCategory on the server
export function updateMaterialCategory(materialCategory) {
  let formData = new FormData();
  formData.append("name", materialCategory.name);
  formData.append("description", materialCategory.description);
  formData.append("online", materialCategory.online);
  if (materialCategory.image && materialCategory.image.name) {
    formData.append("image", materialCategory.image);
  }
  formData.append("industry", materialCategory.industry);
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.put(`${INDUSTRY_URL}${materialCategory.id}/`, formData, headers);
}

// DELETE => delete the materialCategory from the server
export function deleteMaterialCategory(materialCategoryId) {
  return axios.delete(`${INDUSTRY_URL}${materialCategoryId}/`);
}
