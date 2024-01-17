import { createSlice } from '@reduxjs/toolkit';

import { setOpenTooltipId, setIsDroppingFilters, updateLastSelectedMultiTitle } from "./appActions";

const initialState = {
  openTooltipId: '',
  isDroppingFilters: false,
  lastSelectedMulti: [],
}

export const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(setOpenTooltipId, (state, { payload }) => {
        state.openTooltipId = payload;
      })
      .addCase(setIsDroppingFilters, (state, { payload }) => {
        state.isDroppingFilters = payload;
      })
      .addCase(updateLastSelectedMultiTitle, (state, { payload }) => {
        state.lastSelectedMulti = payload;
      })
  },
});