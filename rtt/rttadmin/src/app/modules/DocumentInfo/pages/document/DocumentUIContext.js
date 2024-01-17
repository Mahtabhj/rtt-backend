import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./DocumentUIHelpers";

const DocumentUIContext = createContext();

export function useDocumentUIContext() {
  return useContext(DocumentUIContext);
}

export const DocumentUIConsumer = DocumentUIContext.Consumer;

export function DocumentUIProvider({ documentUIEvents, children }) {
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
    newDocumentButtonClick: documentUIEvents.newDocumentButtonClick,
    openEditDocumentPage: documentUIEvents.openEditDocumentPage,
    openSelectDocumentPage: documentUIEvents.openSelectDocumentPage,
    openDeleteDocumentDialog: documentUIEvents.openDeleteDocumentDialog,
    openFetchDocumentDialog: documentUIEvents.openFetchDocumentDialog,
    openUpdateDocumentStatusDialog:
      documentUIEvents.openUpdateDocumentStatusDialog,
  };

  return (
    <DocumentUIContext.Provider value={value}>
      {children}
    </DocumentUIContext.Provider>
  );
}
