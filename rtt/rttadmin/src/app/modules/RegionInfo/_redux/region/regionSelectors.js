import { createSelector } from '@reduxjs/toolkit';

const regionState = state => state.region;

export const regionSelector = createSelector(regionState, region => region.data);
export const regionIsLoading = createSelector(regionState, regionData => regionData.isLoading);
