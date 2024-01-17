import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./NewsUIHelpers";

const NewsUIContext = createContext();

export function useNewsUIContext() {
  return useContext(NewsUIContext);
}

export const NewsUIConsumer = NewsUIContext.Consumer;

export function NewsUIProvider({ newsUIEvents, children }) {
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
    newNewsButtonClick: newsUIEvents.newNewsButtonClick,
    openEditNewsPage: newsUIEvents.openEditNewsPage,
    openSelectNewsPage: newsUIEvents.openSelectNewsPage,
    openDeleteNewsDialog: newsUIEvents.openDeleteNewsDialog,
    openFetchNewsDialog: newsUIEvents.openFetchNewsDialog,
    openUpdateNewsStatusDialog: newsUIEvents.openUpdateNewsStatusDialog,
  };

  return (
    <NewsUIContext.Provider value={value}>{children}</NewsUIContext.Provider>
  );
}
