import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./IssuingBodyUIHelpers";

const IssuingBodyUIContext = createContext();

export function useIssuingBodyUIContext() {
  return useContext(IssuingBodyUIContext);
}

export const IssuingBodyUIConsumer = IssuingBodyUIContext.Consumer;

export function IssuingBodyUIProvider({ issuingbodyUIEvents, children }) {
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
    newIssuingBodyButtonClick: issuingbodyUIEvents.newIssuingBodyButtonClick,
    openEditIssuingBodyPage: issuingbodyUIEvents.openEditIssuingBodyPage,
    openSelectIssuingBodyPage: issuingbodyUIEvents.openSelectIssuingBodyPage,
    openDeleteIssuingBodyDialog:
      issuingbodyUIEvents.openDeleteIssuingBodyDialog,
    openFetchIssuingBodyDialog: issuingbodyUIEvents.openFetchIssuingBodyDialog,
    openUpdateIssuingBodyStatusDialog:
      issuingbodyUIEvents.openUpdateIssuingBodyStatusDialog,
  };

  return (
    <IssuingBodyUIContext.Provider value={value}>
      {children}
    </IssuingBodyUIContext.Provider>
  );
}
