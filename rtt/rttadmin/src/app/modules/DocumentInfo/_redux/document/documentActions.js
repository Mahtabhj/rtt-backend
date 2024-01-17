import * as documentApiService from "./documentApiService";
import { documentSlice, callTypes } from "./documentSlice";

const { actions } = documentSlice;

export const fetchDocumentList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return documentApiService
    .getDocumentList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.documentListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find document";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchDocument = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.documentFetched({ documentForEdit: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .getDocumentById(id)
    .then((response) => {
      const document = response.data;
      dispatch(actions.documentFetched({ documentForEdit: document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectDocument = (id) => (dispatch) => {
  if (!id) {
    return dispatch(actions.documentSelected({ documentForSelect: undefined }));
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .getDocumentById(id)
    .then((response) => {
      const document = response.data;
      dispatch(actions.documentSelected({ documentForSelect: document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteDocument = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .deleteDocument(id)
    .then((response) => {
      dispatch(actions.documentDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createDocument = (documentForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .createDocument(documentForCreation)
    .then((response) => {
      const document = response.data;
      dispatch(actions.documentCreated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateDocument = (document) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .updateDocument(document)
    .then((response) => {
      dispatch(actions.documentUpdated({ document }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update document";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateDocumentStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return documentApiService
    .updateStatusForDocument(ids, status)
    .then(() => {
      dispatch(actions.documentStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update document status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchDocumentTypeList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return documentApiService
    .getDocumentTypeList(queryParams)
    .then((response) => {
      const totalCount = response.count;
      const entities = response.data.results;
      dispatch(
        actions.documentTypeListFetched({
          totalCount,
          entities,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find product category list";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};
