import { createSlice, isAsyncThunkAction } from '@reduxjs/toolkit'

import { ACTION_TYPE } from '@common';

import {
  addExemption,
  deleteExemptions,
  editExemption,
  getAllExemption,
  getExemptionFilteredIds,
  uploadExemptions
} from './exemptionActions';

const isReadAction = isAsyncThunkAction(getAllExemption, getExemptionFilteredIds);
const isCUDAction = isAsyncThunkAction(addExemption, deleteExemptions, editExemption, uploadExemptions);

const initialState = {
  data: { count: 0, results: [] },
  filteredIds: [],
  isLoading: false,
  isSuccess: false,
  actionsLoading: false
}

export const exemptionSlice = createSlice({
  name: 'exemption',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getAllExemption.fulfilled, (state, { payload }) => {
        state.data = payload;
      })
      .addCase(getExemptionFilteredIds.fulfilled, (state, { payload }) => {
        state.filteredIds = payload;
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
            state.actionsLoading = false
          }
        }
      )
  },
})
