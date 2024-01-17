import { createSelector } from '@reduxjs/toolkit';

const appState = state => state.app;

export const openTooltipIdSelector = createSelector(appState, app => app.openTooltipId);

export const isDroppingFiltersSelector = createSelector(appState, app => app.isDroppingFilters);

export const lastSelectedMultiSelector = createSelector(appState, app => app.lastSelectedMulti);
