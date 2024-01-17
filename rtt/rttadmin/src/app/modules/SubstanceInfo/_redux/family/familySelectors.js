import { createSelector } from "@reduxjs/toolkit";

const familyState = state => state.family;

export const familySelector = createSelector(familyState, family => family.data);

export const familySubstancesSelector = createSelector(familyState, family => family.familySubstances);
export const familySubstancesFilteredIdsSelector = createSelector(familyState, family => family.familySubstancesFilteredIds);

export const familyIsLoading = createSelector(familyState, family => family.isLoading);
export const familyIsSuccess = createSelector(familyState, family => family.isSuccess);

export const familyActionsLoading = createSelector(familyState, family => family.actionsLoading);

