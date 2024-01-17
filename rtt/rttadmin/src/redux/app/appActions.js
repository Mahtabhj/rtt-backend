import { createAction, createAsyncThunk } from "@reduxjs/toolkit";

import { toastInfoProlonged } from "@common";

import * as AppAPI from "./appApiService";
import { lastSelectedMultiSelector } from "./appSelectors";

export const setOpenTooltipId = createAction('app/setOpenTooltip');

export const setIsDroppingFilters = createAction('app/setIsDroppingFilters');

export const updateLastSelectedMultiTitle = createAction('app/updateLastSelectedMultiTitle');

export const getRegulationTaggedCategories = createAsyncThunk(
  'app/getRegulationTaggedCategories',
  async (queryParams, { rejectWithValue }) => {
    try {
      const response = await AppAPI.getRegulationTaggedCategories(queryParams);
      return response.data;
    } catch (e) {
      return rejectWithValue("Can not get regulation tagged categories")
    }
  },
);

export const showLastSelected = createAsyncThunk(
  'app/showLastSelected',
  async ({ selectedId, getToastMessage }, { getState }) => {
    const state = getState();
    const lastSelectedMulti = lastSelectedMultiSelector(state);

    const title = await lastSelectedMulti.find(({ id }) => id === selectedId)?.name;

    return toastInfoProlonged(getToastMessage(title));
  },
);
