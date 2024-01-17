import { createSlice, isAsyncThunkAction } from '@reduxjs/toolkit'

import { ACTION_TYPE, REGION, REGULATION, REGULATORY_FRAMEWORK } from '../../../../common';
import { getRegulationFilterOptions, getRegulatoryFrameworkFilterOptions, getRegionFilterOptions } from './filtersActions';

const isGetOptionsAction = isAsyncThunkAction(getRegulationFilterOptions, getRegulatoryFrameworkFilterOptions, getRegionFilterOptions);

const initialState = {
  [REGULATION]: [],
  [REGULATORY_FRAMEWORK]: [],
  [REGION]: [],
  isLoading: false
}

export const filtersSlice = createSlice({
  name: 'filters',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getRegulationFilterOptions.fulfilled, (state, { payload }) => {
        state[REGULATION] = payload;
      })
      .addCase(getRegulatoryFrameworkFilterOptions.fulfilled, (state, { payload }) => {
        state[REGULATORY_FRAMEWORK] = payload;
      })
      .addCase(getRegionFilterOptions.fulfilled, (state, { payload }) => {
        state[REGION] = payload;
      })
    
      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.PENDING),
        (state, action) => {
          if (isGetOptionsAction(action)) {
            state.isLoading = true;
          }
        }
      )
      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.FULFILLED),
        (state, action) => {
          if (isGetOptionsAction(action)) {
            state.isLoading = false;
          }
        }
      )
      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.REJECTED),
        (state, action ) => {
          if (isGetOptionsAction(action)) {
            state.isLoading = false;
          }
        }
      )
  },
})
