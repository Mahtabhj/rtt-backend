import axios from 'axios';

const BASE_URL = `${process.env.REACT_APP_API_BASE_URI}api/`;
const REGULATION_TAGGED_CATEGORIES = `${BASE_URL}regulation-tagged-product-cat-material-cat/`;

export const getRegulationTaggedCategories = payload => axios.post(`${REGULATION_TAGGED_CATEGORIES}`, payload);
