import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URI + "api/";
const PRODUCT_CATEGORY_URL = BASE_URL + "product-categories/";
const INDUSTRY_URL = BASE_URL + "industries/";

// CREATE =>  POST: add a new productCategory to the server
export function createProductCategory(productCategory) {
  let formData = new FormData();
  formData.append("name", productCategory.name);
  formData.append("description", productCategory.description);
  formData.append("online", productCategory.online);
  formData.append("image", productCategory.image);
  formData.append("parent", productCategory.parent);
  productCategory.industry.forEach((item) => {
    formData.append("industry", item);
  });
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.post(PRODUCT_CATEGORY_URL, formData, headers);
}

// READ
export function getAllProductCategory() {
  return axios.get(PRODUCT_CATEGORY_URL);
}

export function getProductCategoryById(productCategoryId) {
  return axios.get(`${PRODUCT_CATEGORY_URL}${productCategoryId}/`);
}

export function getProductCategoryList(params) {
  return axios.get(PRODUCT_CATEGORY_URL, { params });
}

// UPDATE => PUT: update the productCategory on the server
export function updateProductCategory(productCategory) {
  let formData = new FormData();
  formData.append("name", productCategory.name);
  formData.append("description", productCategory.description);
  formData.append("online", productCategory.online);
  if (productCategory.image && productCategory.image.name) {
    formData.append("image", productCategory.image);
  }
  formData.append("parent", productCategory.parent);
  productCategory.industry.forEach((item) => {
    formData.append("industry", item);
  });
  const headers = { "Content-Type": "multipart/form-data" };
  return axios.put(
    `${PRODUCT_CATEGORY_URL}${productCategory.id}/`,
    formData,
    headers
  );
}

// UPDATE Status
export function updateStatusForProductCategory(ids, status) {
  return axios.post(`${PRODUCT_CATEGORY_URL}updateStatusForProductCategory`, {
    ids,
    status,
  });
}

// DELETE => delete the productCategory from the server
export function deleteProductCategory(productCategoryId) {
  return axios.delete(`${PRODUCT_CATEGORY_URL}${productCategoryId}/`);
}

export function getIndustryList() {
  return axios.get(INDUSTRY_URL);
}
