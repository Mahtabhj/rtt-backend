import { createSlice, isAsyncThunkAction } from '@reduxjs/toolkit'

import { ACTION_TYPE } from '@common';

import { addLimit, deleteLimits, editLimits, getAllLimits, getLimitFilteredIds, getLimitAttributes, uploadLimits } from './limitActions';

const isReadAction = isAsyncThunkAction(getAllLimits, getLimitFilteredIds);
const isCUDAction = isAsyncThunkAction(addLimit, editLimits, deleteLimits, uploadLimits);

const initialState = {
  data: { count: 0, results: [] },
  filteredIds: [],
  isLoading: false,
  isSuccess: false,
  attributes: [],
  actionsLoading: false
}

export const limitSlice = createSlice({
  name: 'limit',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getAllLimits.fulfilled, (state, { payload }) => {
        state.data = payload;
      })
      .addCase(getLimitFilteredIds.fulfilled, (state, { payload }) => {
        state.filteredIds = payload;
      })

      .addCase(getLimitAttributes.fulfilled, (state, { payload }) => {
        state.attributes = payload;
      })

      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.PENDING),
        (state, action) => {
          if (isReadAction(action)) {
              state.isLoading = true;
              state.isSuccess = false;
          }
          if (isCUDAction(action)) {
            state.actionsLoading = true;
          }
        }
      )
      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.FULFILLED),
        (state, action) => {
          if (isReadAction(action)) {
            state.isLoading = false;
            state.isSuccess = true;
          }
          if (isCUDAction(action)) {
            state.actionsLoading = false;
          }
        }
      )
      .addMatcher(
        action => action.type.endsWith(ACTION_TYPE.REJECTED),
        (state, action ) => {
          if (isReadAction(action)) {
            state.isLoading = false;
            state.isSuccess = false;
          }
          if (isCUDAction(action)) {
            state.actionsLoading = false;
          }
        }
      )
  },
})
