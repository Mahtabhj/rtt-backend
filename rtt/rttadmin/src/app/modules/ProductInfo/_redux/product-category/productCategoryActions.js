import * as productCategoryApiService from "./productCategoryApiService";
import { productCategorySlice, callTypes } from "./productCategorySlice";

const { actions } = productCategorySlice;

export const fetchProductCategoryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return productCategoryApiService
    .getProductCategoryList(queryParams)
    .then((response) => {
      const totalCount = response.data.count;
      const entities = response.data.results;
      dispatch(actions.productCategoryListFetched({ totalCount, entities }));
    })
    .catch((error) => {
      error.clientMessage = "Can't find productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.list }));
    });
};

export const fetchProductCategory = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.productCategoryFetched({ productCategoryForEdit: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .getProductCategoryById(id)
    .then((response) => {
      const productCategory = response.data;
      dispatch(
        actions.productCategoryFetched({
          productCategoryForEdit: productCategory,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const selectProductCategory = (id) => (dispatch) => {
  if (!id) {
    return dispatch(
      actions.productCategorySelected({ productCategoryForSelect: undefined })
    );
  }

  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .getProductCategoryById(id)
    .then((response) => {
      const productCategory = response.data;
      dispatch(
        actions.productCategorySelected({
          productCategoryForSelect: productCategory,
        })
      );
    })
    .catch((error) => {
      error.clientMessage = "Can't find productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const deleteProductCategory = (id) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .deleteProductCategory(id)
    .then((response) => {
      dispatch(actions.productCategoryDeleted({ id }));
    })
    .catch((error) => {
      error.clientMessage = "Can't delete productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const createProductCategory = (productCategoryForCreation) => (
  dispatch
) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .createProductCategory(productCategoryForCreation)
    .then((response) => {
      const productCategory = response.data;
      dispatch(actions.productCategoryCreated({ productCategory }));
    })
    .catch((error) => {
      error.clientMessage = "Can't create productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateProductCategory = (productCategory) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .updateProductCategory(productCategory)
    .then(() => {
      dispatch(actions.productCategoryUpdated({ productCategory }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update productCategory";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const updateProductCategoryStatus = (ids, status) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.action }));
  return productCategoryApiService
    .updateStatusForProductCategory(ids, status)
    .then(() => {
      dispatch(actions.productCategoryStatusUpdated({ ids, status }));
    })
    .catch((error) => {
      error.clientMessage = "Can't update productCategory status";
      dispatch(actions.catchError({ error, callType: callTypes.action }));
    });
};

export const fetchIndustryList = (queryParams) => (dispatch) => {
  dispatch(actions.startCall({ callType: callTypes.list }));
  return productCategoryApiService
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
