import React, { createContext, useContext, useState, useCallback } from "react";
import { isEqual, isFunction } from "lodash";
import { initialFilter } from "./ImpactAssessmentUIHelpers";

const ImpactAssessmentUIContext = createContext();

export function useImpactAssessmentUIContext() {
  return useContext(ImpactAssessmentUIContext);
}

export const ImpactAssessmentUIConsumer = ImpactAssessmentUIContext.Consumer;

export function ImpactAssessmentUIProvider({
  impactAssessmentUIEvents,
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
    newImpactAssessmentButtonClick:
      impactAssessmentUIEvents.newImpactAssessmentButtonClick,
    openEditImpactAssessmentPage:
      impactAssessmentUIEvents.openEditImpactAssessmentPage,
    openSelectImpactAssessmentPage:
      impactAssessmentUIEvents.openSelectImpactAssessmentPage,
    openDeleteImpactAssessmentDialog:
      impactAssessmentUIEvents.openDeleteImpactAssessmentDialog,
    openFetchImpactAssessmentDialog:
      impactAssessmentUIEvents.openFetchImpactAssessmentDialog,
    openUpdateImpactAssessmentStatusDialog:
      impactAssessmentUIEvents.openUpdateImpactAssessmentStatusDialog,
  };

  return (
    <ImpactAssessmentUIContext.Provider value={value}>
      {children}
    </ImpactAssessmentUIContext.Provider>
  );
}
