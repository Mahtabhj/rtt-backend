import { createSelector } from '@reduxjs/toolkit';

const filtersState = state => state.filters;

export const filtersSelector = createSelector(filtersState, filters => filters);

export const filtersIsLoading = createSelector(filtersState, filters => filters.isLoading);
