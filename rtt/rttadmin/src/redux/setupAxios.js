import { toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

toast.configure()

const showErrorMessage = message => message && toast.error(message, { position: toast.POSITION.TOP_CENTER });

export default function setupAxios(axios, store) {

  // Axios Request Interceptor
  axios.interceptors.request.use(
    config => {
      const {
        auth: { authToken }
      } = store.getState();

      if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
      }
      return config;
    },
    err => Promise.reject(err)
  );

  // Axios Response Interceptor
  axios.interceptors.response.use(
    response => response,
    error => {
      const { status, data } = error.response;

      if (status === 400 && data) {
        // todo check all possible BE response error status codes and data
        const message = data[Object.keys(data)[0]][0];
        if (Array.isArray(data[Object.keys(data)[0]])) showErrorMessage(message);
      } else if (status === 403) {
        window.location = '/backend/logout';
      } else if (status === 424) {
        showErrorMessage('Linked item can not be deleted');
      } else if (status === 500) {
        showErrorMessage('Server Error');
      }
      return Promise.reject(error);
  });

}
