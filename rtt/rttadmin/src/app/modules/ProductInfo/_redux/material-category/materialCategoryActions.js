import * as materialCategoryApiService from "./materialCategoryApiService";
import { materialCategorySlice, callTypes } from "./materialCategorySlice";

const { actions } = materialCategorySlice;

export const fetchMaterialCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return materialCategoryApiService
    .getMaterialCategoryList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.materialCategoryListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find materialCategory";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchMaterialCategory = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.materialCategoryFetched({ materialCategoryForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return materialCategoryApiService
    .getMaterialCategoryById(id)
    .then((response) => {
      const materialCategory = response.data;
      dispatch(
        actions.materialCategoryFetched({ materialCategoryForEdit: materialCategory })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find materialCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteMaterialCategory = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return materialCategoryApiService
    .deleteMaterialCategory(id)
    .then((response) => {
      dispatch(actions.materialCategoryDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete materialCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createMaterialCategory = (materialCategoryForCreation) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return materialCategoryApiService
    .createMaterialCategory(materialCategoryForCreation)
    .then((response) => {
      const materialCategory = response.data;
      dispatch(actions.materialCategoryCreated({ materialCategory }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create materialCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateMaterialCategory = (materialCategory) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return materialCategoryApiService
    .updateMaterialCategory(materialCategory)
    .then(() => {
      dispatch(actions.materialCategoryUpdated({ materialCategory }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update materialCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};