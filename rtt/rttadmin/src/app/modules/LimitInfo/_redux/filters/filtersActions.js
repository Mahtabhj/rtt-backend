import { createAsyncThunk } from '@reduxjs/toolkit';
import { toast } from "react-toastify";

import * as FiltersAPI from "./filtersApiService";

export const getRegulationFilterOptions = createAsyncThunk(
  'filters/regulations',
  async (keyword, { rejectWithValue }) => {
    try {
      const response = await FiltersAPI.getRegulationFilter(keyword);
      return response.data;
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const getRegulatoryFrameworkFilterOptions = createAsyncThunk(
  'filters/frameworks',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await FiltersAPI.getRegulatoryFrameworkFilter(dataToSend);
      return response.data;
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);

export const getRegionFilterOptions = createAsyncThunk(
  'filters/regions',
  async (dataToSend, { rejectWithValue }) => {
    try {
      const response = await FiltersAPI.getRegionFilter(dataToSend);
      return response.data;
    } catch (err) {
      toast.error(err.response.data.message || 'Something went wrong')
      return rejectWithValue(err.response.data.error);
    }
  },
);
