import { createSlice, isAsyncThunkAction } from '@reduxjs/toolkit'

import { ACTION_TYPE } from '@common';

import {
  addFamily,
  addFamilySubstances,
  editFamily,
  deleteFamily,
  getAllFamilies,
  getFamilyForEdit,
  getFamilySubstances,
  getFamilySubstancesFilteredIds,
  uploadFamilySubstances,
  deleteFamilySubstance
} from './familyActions';

const isReadAction = isAsyncThunkAction(getAllFamilies, getFamilySubstances);
const isCUDAction = isAsyncThunkAction(
  addFamily,
  editFamily,
  getFamilyForEdit,
  deleteFamily,
  addFamilySubstances,
  uploadFamilySubstances,
  deleteFamilySubstance
);

const initialState = {
  data: { count: 0, results: [] },
  familySubstances: { count: 0, results: [] },
  familySubstancesFilteredIds: [],
  isLoading: false,
  isSuccess: false,
  actionsLoading: false
}

export const familySlice = createSlice({
  name: 'family',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(getAllFamilies.fulfilled, (state, { payload }) => {
        state.data = payload;
      })
      .addCase(getFamilySubstances.fulfilled, (state, { payload }) => {
        state.familySubstances = payload;
      })
      .addCase(getFamilySubstancesFilteredIds.fulfilled, (state, { payload }) => {
        state.familySubstancesFilteredIds = payload;
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
