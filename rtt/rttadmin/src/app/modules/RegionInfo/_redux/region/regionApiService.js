import axios from 'axios';

const BASE_URL = `${process.env.REACT_APP_API_BASE_URI}api`;
const REGIONS_URL = `${BASE_URL}/es/react-admin-active-region-page/`;

export const getRegions = () => axios.get(`${REGIONS_URL}`);