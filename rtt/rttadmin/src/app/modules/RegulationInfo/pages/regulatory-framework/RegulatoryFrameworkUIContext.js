import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./RegulatoryFrameworkUIHelpers";

const RegulatoryFrameworkUIContext = createContext();

export function useRegulatoryFrameworkUIContext() {
  return useContext(RegulatoryFrameworkUIContext);
}

export const RegulatoryFrameworkUIConsumer =
  RegulatoryFrameworkUIContext.Consumer;

export function RegulatoryFrameworkUIProvider({
  regulatoryFrameworkUIEvents,
  children,
}) {
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
    newRegulatoryFrameworkButtonClick:
      regulatoryFrameworkUIEvents.newRegulatoryFrameworkButtonClick,
    openEditRegulatoryFrameworkPage:
      regulatoryFrameworkUIEvents.openEditRegulatoryFrameworkPage,
    openSelectRegulatoryFrameworkPage:
      regulatoryFrameworkUIEvents.openSelectRegulatoryFrameworkPage,
    openDeleteRegulatoryFrameworkDialog:
      regulatoryFrameworkUIEvents.openDeleteRegulatoryFrameworkDialog,
    openFetchRegulatoryFrameworkDialog:
      regulatoryFrameworkUIEvents.openFetchRegulatoryFrameworkDialog,
    openUpdateRegulatoryFrameworkStatusDialog:
      regulatoryFrameworkUIEvents.openUpdateRegulatoryFrameworkStatusDialog,
  };

  return (
    <RegulatoryFrameworkUIContext.Provider value={value}>
      {children}
    </RegulatoryFrameworkUIContext.Provider>
  );
}
