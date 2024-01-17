import * as issuingbodyApiService from "./issuingbodyApiService";
import { issuingbodySlice, callTypes } from "./issuingbodySlice";

const { actions } = issuingbodySlice;

export const fetchIssuingBodyList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return issuingbodyApiService
    .getIssuingBodyList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.issuingbodyListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchIssuingBody = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.issuingbodyFetched({ issuingbodyForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .getIssuingBodyById(id)
    .then((response) => {
      const issuingbody = response.data;
      dispatch(actions.issuingbodyFetched({ issuingbodyForEdit: issuingbody }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectIssuingBody = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.issuingbodySelected({ issuingbodyForSelect: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .getIssuingBodyById(id)
    .then((response) => {
      const issuingbody = response.data;
      dispatch(
        actions.issuingbodySelected({ issuingbodyForSelect: issuingbody })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteIssuingBody = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .deleteIssuingBody(id)
    .then((response) => {
      dispatch(actions.issuingbodyDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createIssuingBody = (issuingbodyForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .createIssuingBody(issuingbodyForCreation)
    .then((response) => {
      const issuingbody = response.data;
      dispatch(actions.issuingbodyCreated({ issuingbody }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateIssuingBody = (issuingbody) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .updateIssuingBody(issuingbody)
    .then(() => {
      dispatch(actions.issuingbodyUpdated({ issuingbody }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update issuingbody";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateIssuingBodyStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return issuingbodyApiService
    .updateStatusForIssuingBody(ids, status)
    .then(() => {
      dispatch(actions.issuingbodyStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update issuingbody status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchRegionList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return issuingbodyApiService
    .getRegionList(queryParams)
    .then((response) => {
      const regionList = response.data.results;
      dispatch(actions.regionListFetched({ regionList }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find region";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchURLsList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return issuingbodyApiService
    .getURLsList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.urlListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};
