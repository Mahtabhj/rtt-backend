import { createSelector } from '@reduxjs/toolkit';

const substanceDataState = state => state.substanceData;

export const substanceDataSelector = createSelector(substanceDataState,substanceData => substanceData.data);
export const substanceDataFilteredIdsSelector = createSelector(substanceDataState, substanceData => substanceData.filteredIds);

export const substanceDataIsLoading = createSelector(substanceDataState, substanceData => substanceData.isLoading);
export const substanceDataIsSuccess = createSelector(substanceDataState, substanceData => substanceData.isSuccess);

export const substanceDataActionsLoading = createSelector(substanceDataState, substanceData => substanceData.actionsLoading);

export const propertyListSelector = createSelector(substanceDataState,substanceData => substanceData.propertyList);
