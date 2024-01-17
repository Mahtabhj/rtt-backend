import { createSelector } from '@reduxjs/toolkit';

const exemptionState = state => state.exemption;

export const exemptionSelector = createSelector(exemptionState,exemption => exemption.data);
export const exemptionFilteredIdsSelector = createSelector(exemptionState,exemption => exemption.filteredIds);

export const exemptionIsLoading = createSelector(exemptionState, exemption => exemption.isLoading);
export const exemptionIsSuccess = createSelector(exemptionState, exemption => exemption.isSuccess);

export const exemptionActionsLoading = createSelector(exemptionState, exemption => exemption.actionsLoading);
