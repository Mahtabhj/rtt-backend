import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./RegulationUIHelpers";

const RegulationUIContext = createContext();

export function useRegulationUIContext() {
  return useContext(RegulationUIContext);
}

export const RegulationUIConsumer = RegulationUIContext.Consumer;

export function RegulationUIProvider({ regulationUIEvents, children }) {
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
    newRegulationButtonClick: regulationUIEvents.newRegulationButtonClick,
    openEditRegulationPage: regulationUIEvents.openEditRegulationPage,
    openSelectRegulationPage: regulationUIEvents.openSelectRegulationPage,
    openDeleteRegulationDialog: regulationUIEvents.openDeleteRegulationDialog,
    openFetchRegulationDialog: regulationUIEvents.openFetchRegulationDialog,
    openUpdateRegulationStatusDialog:
      regulationUIEvents.openUpdateRegulationStatusDialog,
  };

  return (
    <RegulationUIContext.Provider value={value}>
      {children}
    </RegulationUIContext.Provider>
  );
}
