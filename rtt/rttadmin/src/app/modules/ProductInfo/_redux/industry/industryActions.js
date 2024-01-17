import * as industryApiService from "./industryApiService";
import { industrySlice, callTypes } from "./industrySlice";

const { actions } = industrySlice;

export const fetchIndustryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return industryApiService
    .getIndustryList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.industryListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find industry";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchIndustry = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.industryFetched({ industryForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .getIndustryById(id)
    .then((response) => {
      const industry = response.data;
      dispatch(
        actions.industryFetched({ industryForEdit: industry })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find industry";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectIndustry = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.industrySelected({ industryForSelect: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .getIndustryById(id)
    .then((response) => {
      const industry = response.data;
      dispatch(
        actions.industrySelected({ industryForSelect: industry })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find industry";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteIndustry = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .deleteIndustry(id)
    .then((response) => {
      dispatch(actions.industryDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete industry";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createIndustry = (industryForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .createIndustry(industryForCreation)
    .then((response) => {
      const industry = response.data;
      dispatch(actions.industryCreated({ industry }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create industry";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateIndustry = (industry) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .updateIndustry(industry)
    .then(() => {
      dispatch(actions.industryUpdated({ industry }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update industry";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateIndustryStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return industryApiService
    .updateStatusForIndustry(ids, status)
    .then(() => {
      dispatch(actions.industryStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update industry status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};
