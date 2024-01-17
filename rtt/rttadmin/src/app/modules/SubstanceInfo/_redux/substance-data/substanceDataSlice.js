import { createSlice, isAsyncThunkAction } from '@reduxjs/toolkit'

import { ACTION_TYPE } from '@common';

import {
  addSubstanceData,
  getAllSubstanceData,
  getProperties,
  getSubstanceDataFilteredIds,
  uploadSubstanceData,
} from './substanceDataActions';

const isReadAction = isAsyncThunkAction(getAllSubstanceData, getSubstanceDataFilteredIds);
const isCUDAction = isAsyncThunkAction(addSubstanceData, uploadSubstanceData);

const initialState = {
  data: { count: 0, results: [] },
  filteredIds: [],
  propertyList: [],
  isLoading: false,
  isSuccess: false,
  actionsLoading: false
}

export const substanceDataSlice = createSlice({
  name: 'substanceData',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getAllSubstanceData.fulfilled, (state, { payload }) => {
        state.data = payload;
      })
      .addCase(getSubstanceDataFilteredIds.fulfilled, (state, { payload }) => {
        state.filteredIds = payload;
      })
      .addCase(getProperties.fulfilled, (state, { payload }) => {
        state.propertyList = payload;
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
