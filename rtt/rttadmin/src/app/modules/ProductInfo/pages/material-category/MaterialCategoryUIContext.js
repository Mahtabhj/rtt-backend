import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./MaterialCategoryUIHelpers";

const MaterialCategoryUIContext = createContext();

export function useMaterialCategoryUIContext() {
  return useContext(MaterialCategoryUIContext);
}

export const MaterialCategoryUIConsumer = MaterialCategoryUIContext.Consumer;

export function MaterialCategoryUIProvider({ materialCategoryUIEvents, children }) {
  const [queryParams, setQueryParamsBase] = useState(initialFilter);
  const [ids, setIds] = useState([]);

  const setQueryParams = useCallback((nextQueryParams) => {
    setQueryParamsBase((prevQueryParams) => {
      if (isFunction(nextQueryParams)) {
        nextQueryParams = nextQueryParams(prevQueryParams);
      }
      if (isEqual(prevQueryParams, nextQueryParams)) {
        return prevQueryParams;
      }
      return nextQueryParams;
    });
  }, []);


  const value = {
    queryParams,
    setQueryParamsBase,
    ids,
    setIds,
    setQueryParams,
    newMaterialCategoryButtonClick: materialCategoryUIEvents.newMaterialCategoryButtonClick,
    openEditMaterialCategoryPage: materialCategoryUIEvents.openEditMaterialCategoryPage,
    openDeleteMaterialCategoryDialog: materialCategoryUIEvents.openDeleteMaterialCategoryDialog,
    openFetchMaterialCategoryDialog: materialCategoryUIEvents.openFetchMaterialCategoryDialog,
  };

  return (
    <MaterialCategoryUIContext.Provider value={value}>
      {children}
    </MaterialCategoryUIContext.Provider>
  );
}
