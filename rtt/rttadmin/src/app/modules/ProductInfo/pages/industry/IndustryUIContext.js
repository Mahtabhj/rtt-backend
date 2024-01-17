import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./IndustryUIHelpers";

const IndustryUIContext = createContext();

export function useIndustryUIContext() {
  return useContext(IndustryUIContext);
}

export const IndustryUIConsumer = IndustryUIContext.Consumer;

export function IndustryUIProvider({ industryUIEvents, children }) {
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
    newIndustryButtonClick: industryUIEvents.newIndustryButtonClick,
    openEditIndustryPage: industryUIEvents.openEditIndustryPage,
    openDeleteIndustryDialog: industryUIEvents.openDeleteIndustryDialog,
    openFetchIndustryDialog: industryUIEvents.openFetchIndustryDialog,
  };

  return (
    <IndustryUIContext.Provider value={value}>
      {children}
    </IndustryUIContext.Provider>
  );
}
