import * as substancesApiService from "./substancesApiService";
import { substancesSlice, callTypes } from "./substancesSlice";
import { toast } from "react-toastify";

const { actions } = substancesSlice;

export const fetchRelatedSubstances = queryParams => dispatch => {
  dispatch(actions.startCall({ callType: callTypes.list }));

  return substancesApiService
    .getRelatedSubstancesPaginated(queryParams)
    .then((response) => {
      const { count, results } = response.data;
      const { skip, limit, ...entityQuery } = queryParams;

      dispatch(actions.relatedSubstancesFetched({ count, results, entityQuery }));
    })
    .catch((error) => {
      error.clientMessage = "Can't get related substances";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const addOrRemoveSubstancesManually = dataToSend => (dispatch, getState) => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  const state = getState();
  const { entityQuery } = state.substances;

  return substancesApiService
    .addOrRemoveSubstances({ ...dataToSend, ...entityQuery })
    .then((response) => {
      toast.success(response.data.message, { position: toast.POSITION.TOP_RIGHT });
      dispatch(actions.substancesAddedManual({}));
    })
    .catch((error) => {
      error.clientMessage = "Can't add substances";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const addSubstancesUpload = (file, setProgress) => (dispatch, getState) => {
  dispatch(actions.startCall({ callType: callTypes.action }));

  const state = getState();
  const { entityQuery } = state.substances;
  const [ entityQueryKey, entityQueryValue ] = Object.entries(entityQuery)[0];

  const formData = new FormData();

  formData.append('file', file);
  formData.append(entityQueryKey, entityQueryValue.toString());

  const config = {
    'Content-Type': 'multipart/form-data',
    'onUploadProgress': ({ loaded, total }) => setProgress(+((100 * loaded) / total).toFixed()),
  };

  return substancesApiService
    .addSubstanceUpload(formData, config)
    .then((response) => {
      toast.success(response.data.message, { position: toast.POSITION.TOP_RIGHT });
      dispatch(actions.substancesUploaded({}));
    })
    .catch((error) => {
      error.clientMessage = "Can't upload substances";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};