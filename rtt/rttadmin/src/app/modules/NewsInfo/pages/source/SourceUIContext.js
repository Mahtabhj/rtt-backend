import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./SourceUIHelpers";

const SourceUIContext = createContext();

export function useSourceUIContext() {
  return useContext(SourceUIContext);
}

export const SourceUIConsumer = SourceUIContext.Consumer;

export function SourceUIProvider({ sourceUIEvents, children }) {
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
    newSourceButtonClick: sourceUIEvents.newSourceButtonClick,
    openEditSourcePage: sourceUIEvents.openEditSourcePage,
    openSelectSourcePage: sourceUIEvents.openSelectSourcePage,
    openDeleteSourceDialog: sourceUIEvents.openDeleteSourceDialog,
    openFetchSourceDialog: sourceUIEvents.openFetchSourceDialog,
    openUpdateSourceStatusDialog: sourceUIEvents.openUpdateSourceStatusDialog,
  };

  return (
    <SourceUIContext.Provider value={value}>
      {children}
    </SourceUIContext.Provider>
  );
}
