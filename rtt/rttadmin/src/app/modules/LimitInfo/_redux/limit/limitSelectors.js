import {createSelector} from '@reduxjs/toolkit';

const limitState = state => state.limit;

export const limitSelector = createSelector(limitState,limit => limit.data);
export const limitFilteredIdsSelector = createSelector(limitState,limit => limit.filteredIds);

export const limitIsLoading = createSelector(limitState, limit => limit.isLoading);
export const limitIsSuccess = createSelector(limitState, limit => limit.isSuccess);

export const limitActionsLoading = createSelector(limitState, limit => limit.actionsLoading);

export const limitAttributesSelector = createSelector(limitState,limit => limit.attributes);
