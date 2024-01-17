import * as sourceApiService from "./sourceApiService";
import { sourceSlice, callTypes } from "./sourceSlice";

const { actions } = sourceSlice;

export const fetchSourceList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return sourceApiService
    .getSourceList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.sourceListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find source";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchSourceTypeList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return sourceApiService
    .getSourceTypeList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.sourceTypeListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find source type";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchSource = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.sourceFetched({ sourceForEdit: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .getSourceById(id)
    .then((response) => {
      const source = response.data;
      dispatch(actions.sourceFetched({ sourceForEdit: source }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find source";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectSource = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.sourceSelected({ sourceForSelect: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .getSourceById(id)
    .then((response) => {
      const source = response.data;
      dispatch(actions.sourceSelected({ sourceForSelect: source }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find source";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteSource = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .deleteSource(id)
    .then((response) => {
      dispatch(actions.sourceDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete source";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createSource = (sourceForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .createSource(sourceForCreation)
    .then((response) => {
      const source = response.data;
      dispatch(actions.sourceCreated({ source }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create source";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateSource = (source) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .updateSource(source)
    .then((response) => {
      dispatch(actions.sourceUpdated({ source }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update source";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateSourceStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return sourceApiService
    .updateStatusForSource(ids, status)
    .then(() => {
      dispatch(actions.sourceStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update source status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};
