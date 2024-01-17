import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./OrganizationUIHelpers";

const OrganizationUIContext = createContext();

export function useOrganizationUIContext() {
  return useContext(OrganizationUIContext);
}

export const OrganizationUIConsumer = OrganizationUIContext.Consumer;

export function OrganizationUIProvider({ organizationUIEvents, children }) {
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
    newOrganizationButtonClick: organizationUIEvents.newOrganizationButtonClick,
    openEditOrganizationPage: organizationUIEvents.openEditOrganizationPage,
    openSelectOrganizationPage: organizationUIEvents.openSelectOrganizationPage,
    openDeleteOrganizationDialog: organizationUIEvents.openDeleteOrganizationDialog,
    openFetchOrganizationDialog: organizationUIEvents.openFetchOrganizationDialog,
    openUpdateOrganizationStatusDialog: organizationUIEvents.openUpdateOrganizationStatusDialog,
  };

  return (
    <OrganizationUIContext.Provider value={value}>
      {children}
    </OrganizationUIContext.Provider>
  );
}
